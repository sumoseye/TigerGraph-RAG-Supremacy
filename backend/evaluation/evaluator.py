# backend/evaluation/evaluator.py
import os
import json
import asyncio
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime
from app.config import settings
from difflib import SequenceMatcher

print(f"\n{'='*70}")
print(f"INITIALIZING EVALUATION MODULE")
print(f"{'='*70}")

# Setup - Import BEFORE initialization
try:
    from huggingface_hub import InferenceClient
    print("✅ HuggingFace Hub imported")
except ImportError as e:
    print(f"❌ Failed to import HF Hub: {e}")
    raise

try:
    import evaluate
    print("✅ Evaluate library imported")
except ImportError as e:
    print(f"❌ Failed to import evaluate: {e}")
    raise

# GLOBAL state dictionary to track initialization
_eval_state = {
    "hf_client": None,
    "bertscore": None,
    "initialized": False
}


def _initialize_tools():
    """Initialize tools only once"""
    global _eval_state
    
    if _eval_state["initialized"]:
        print("✅ Tools already initialized")
        return
    
    # Initialize HF Client
    if settings.HF_TOKEN:
        try:
            print("⏳ Initializing LLM Judge (Llama 3.1 8B)...")
            _eval_state["hf_client"] = InferenceClient(
                model="meta-llama/Llama-3.1-8B-Instruct",
                token=settings.HF_TOKEN
            )
            print(f"✅ LLM Judge ready")
        except Exception as e:
            print(f"❌ LLM Judge failed: {e}")
            _eval_state["hf_client"] = None
    else:
        print(f"❌ HF_TOKEN not set")
    
    # Initialize BERTScore - WITH DEBUGGING
    try:
        print("⏳ Loading BERTScore...")
        bertscore_obj = evaluate.load("bertscore")
        
        print(f"   Type: {type(bertscore_obj)}")
        print(f"   Is None: {bertscore_obj is None}")
        print(f"   Bool value: {bool(bertscore_obj)}")
        print(f"   Has compute: {hasattr(bertscore_obj, 'compute')}")
        
        _eval_state["bertscore"] = bertscore_obj
        
        # Test it immediately
        if bertscore_obj and hasattr(bertscore_obj, 'compute'):
            print("✅ BERTScore loaded and callable")
        else:
            print("⚠️  BERTScore loaded but may not work")
            
    except Exception as e:
        print(f"❌ BERTScore load failed: {e}")
        import traceback
        traceback.print_exc()
        _eval_state["bertscore"] = None
    
    _eval_state["initialized"] = True
    
    print(f"\n{'='*70}")
    print(f"INITIALIZATION STATUS:")
    print(f"  LLM Judge: {'✅ Ready' if _eval_state['hf_client'] else '❌ Not available'}")
    print(f"  BERTScore object: {_eval_state['bertscore']}")
    print(f"  BERTScore type: {type(_eval_state['bertscore'])}")
    print(f"  BERTScore ready: {'✅ Ready' if (_eval_state['bertscore'] is not None) else '❌ Not available'}")
    print(f"  Initialized: {_eval_state['initialized']}")
    print(f"{'='*70}\n")


# Initialize on module load
_initialize_tools()

# Judge prompt
JUDGE_PROMPT = """Grade the system's answer.

Question: {q}
Correct answer: {correct}
System answer: {answer}

Reply with only PASS or FAIL.

PASS = the system answer correctly addresses the question with no major errors.
FAIL = the answer is wrong, missing, or contradicts the correct answer."""


def similarity_ratio(a: str, b: str) -> float:
    """Calculate similarity between two strings"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def load_ground_truth() -> List[Dict]:
    """Load ground truth questions"""
    truth_path = settings.EVALUATION_PATH / "ground_truth.json"
    
    if not truth_path.exists():
        print(f"❌ Ground truth not found at {truth_path}")
        return []
    
    try:
        with open(truth_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ Loaded {len(data)} ground truth Q&A pairs")
        return data
    except Exception as e:
        print(f"❌ Error loading ground truth: {e}")
        return []


def find_best_match(query: str, ground_truth_list: List[Dict]) -> Optional[Dict]:
    """Find the best matching ground truth for a query"""
    if not ground_truth_list:
        return None
    
    best_match = None
    best_score = 0.0
    
    query_lower = query.lower().strip()
    
    for gt in ground_truth_list:
        question = gt.get("question", "").lower().strip()
        score = similarity_ratio(query_lower, question)
        
        query_words = set(query_lower.split())
        question_words = set(question.split())
        keyword_overlap = len(query_words & question_words) / max(len(query_words), 1)
        
        combined_score = (score * 0.7) + (keyword_overlap * 0.3)
        
        if combined_score > best_score:
            best_score = combined_score
            best_match = gt
    
    if best_match and best_score > 0.3:
        print(f"📍 Best match (score: {best_score:.2f})")
        return best_match
    
    print(f"⚠️  No good match found (best: {best_score:.2f})")
    return None


async def evaluate_pipeline_results(query: str, p1_answer: str, p2_answer: str, p3_answer: str) -> Dict[str, Any]:
    """
    Evaluate results from all 3 pipelines using LLM Judge + BERTScore.
    """
    
    print(f"\n{'='*70}")
    print(f"🔍 EVALUATION STARTING")
    print(f"{'='*70}")
    print(f"Query: {query}")
    print(f"P1 length: {len(p1_answer)} chars")
    print(f"P2 length: {len(p2_answer)} chars")
    print(f"P3 length: {len(p3_answer)} chars")
    
    # Ensure tools are initialized
    if not _eval_state["initialized"]:
        print("⏳ Tools not initialized, initializing now...")
        _initialize_tools()
    
    # Load ground truth
    ground_truth_list = load_ground_truth()
    
    if not ground_truth_list:
        print("⚠️  No ground truth available, using fallback evaluation")
        return await fallback_evaluation(p1_answer, p2_answer, p3_answer)
    
    # Find matching ground truth
    best_match = find_best_match(query, ground_truth_list)
    
    if not best_match:
        print("⚠️  No matching ground truth, using fallback evaluation")
        return await fallback_evaluation(p1_answer, p2_answer, p3_answer)
    
    correct_answer = best_match.get("correct_answer", "")
    pipeline_outputs = [p1_answer, p2_answer, p3_answer]
    
    # Run evaluations
    results = await evaluate_with_judges(
        query=query,
        correct_answer=correct_answer,
        pipeline_outputs=pipeline_outputs
    )
    
    print(f"\n{'='*70}")
    print(f"✅ EVALUATION COMPLETE")
    print(f"{'='*70}\n")
    
    return results


async def fallback_evaluation(p1: str, p2: str, p3: str) -> Dict[str, Any]:
    """Simple evaluation when no ground truth is available"""
    
    def calculate_quality_score(response: str) -> float:
        """Calculate quality score based on length and structure"""
        length_score = min(50, len(response) / 100)
        has_structure = 50 if any(marker in response for marker in ["•", "-", "1.", "\n\n"]) else 25
        return min(100, length_score + has_structure)
    
    p1_score = calculate_quality_score(p1)
    p2_score = calculate_quality_score(p2)
    p3_score = calculate_quality_score(p3)
    
    return {
        "llm_judge_p1": round(p1_score / 100, 2),
        "llm_judge_p2": round(p2_score / 100, 2),
        "llm_judge_p3": round(p3_score / 100, 2),
        "bertscore_p1": round(p1_score / 100, 4),
        "bertscore_p2": round(p2_score / 100, 4),
        "bertscore_p3": round(p3_score / 100, 4),
        "note": "Fallback evaluation (no ground truth)"
    }


async def evaluate_with_judges(query: str, correct_answer: str, pipeline_outputs: List[str]) -> Dict[str, Any]:
    """Evaluate using LLM Judge and BERTScore"""
    
    judge_results = []
    bert_scores = []
    
    # LLM Judge evaluation
    print("\n" + "="*70)
    print("LLM-as-a-Judge Evaluation (Llama 3.1 8B)")
    print("="*70)
    
    if _eval_state["hf_client"]:
        for i, output in enumerate(pipeline_outputs):
            pipeline_name = ["Pipeline 1 (LLM Only)", "Pipeline 2 (RAG)", "Pipeline 3 (Multi-Agent)"][i]
            
            prompt = JUDGE_PROMPT.format(
                q=query,
                correct=correct_answer,
                answer=output
            )
            
            try:
                print(f"⏳ {pipeline_name}: Calling judge...")
                
                verdict = _eval_state["hf_client"].chat_completion(
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=10,
                    temperature=0.0
                )
                
                verdict_text = verdict.choices[0].message.content.strip().upper()
                is_pass = "PASS" in verdict_text
                judge_results.append(is_pass)  # ← Store boolean, not float
                
                print(f"   {'✓ PASS' if is_pass else '✗ FAIL'} ({verdict_text})")
                
            except Exception as e:
                print(f"   ❌ Judge error: {e}")
                judge_results.append(None)
    else:
        print("⚠️  LLM Judge not available")
        judge_results = [None, None, None]
    
    # BERTScore evaluation - IMPROVED CHECK
    print("\n" + "="*70)
    print("BERTScore Evaluation (Raw F1)")
    print("="*70)
    
    print(f"🔍 Debug:")
    print(f"   _eval_state['bertscore']: {_eval_state['bertscore']}")
    print(f"   Type: {type(_eval_state['bertscore'])}")
    print(f"   Is None: {_eval_state['bertscore'] is None}")
    print(f"   Has compute: {hasattr(_eval_state['bertscore'], 'compute') if _eval_state['bertscore'] else False}")
    
    if _eval_state["bertscore"] is not None and hasattr(_eval_state["bertscore"], 'compute'):
        try:
            print("⏳ Computing BERTScore...")
            
            bert_results = _eval_state["bertscore"].compute(
                predictions=pipeline_outputs,
                references=[correct_answer, correct_answer, correct_answer],
                lang="en",
                rescale_with_baseline=False,  # Raw scores
                idf=False,
                batch_size=1
            )
            
            bert_scores = bert_results["f1"]
            
            print(f"\n✅ BERTScore Results:")
            for i, score in enumerate(bert_scores):
                pipeline_name = ["Pipeline 1 (LLM Only)", "Pipeline 2 (RAG)", "Pipeline 3 (Multi-Agent)"][i]
                print(f"   {pipeline_name}: {score:.4f}")
            
        except Exception as e:
            print(f"❌ BERTScore computation failed: {e}")
            import traceback
            traceback.print_exc()
            
            print(f"\n⚠️  Using similarity-based fallback...")
            bert_scores = []
            for output in pipeline_outputs:
                similarity = similarity_ratio(correct_answer, output)
                bert_scores.append(similarity)
    else:
        print("❌ BERTScore not available (object is None or missing compute method)")
        print("\n⚠️  Using similarity-based fallback...")
        bert_scores = []
        for output in pipeline_outputs:
            similarity = similarity_ratio(correct_answer, output)
            bert_scores.append(similarity)
    
    print("="*70)
    
    return {
        "llm_judge_p1": judge_results[0],  # Return boolean or None
        "llm_judge_p2": judge_results[1],
        "llm_judge_p3": judge_results[2],
        "bertscore_p1": round(float(bert_scores[0]), 4) if len(bert_scores) > 0 else None,
        "bertscore_p2": round(float(bert_scores[1]), 4) if len(bert_scores) > 1 else None,
        "bertscore_p3": round(float(bert_scores[2]), 4) if len(bert_scores) > 2 else None,
    }