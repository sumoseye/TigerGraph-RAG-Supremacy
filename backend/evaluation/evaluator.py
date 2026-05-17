# backend/evaluation/evaluator.py
import os
import json
from typing import Dict, Any, List, Optional
from pathlib import Path
from app.config import settings
from difflib import SequenceMatcher

print(f"\n{'='*70}")
print(f"INITIALIZING EVALUATION MODULE")
print(f"{'='*70}")
print(f"HF_TOKEN: {settings.HF_TOKEN[:20] if settings.HF_TOKEN else 'MISSING'}...")
print(f"EVALUATION_PATH: {settings.EVALUATION_PATH}")
print(f"EVALUATION_PATH exists: {settings.EVALUATION_PATH.exists()}")

# Setup
try:
    from huggingface_hub import InferenceClient
    import evaluate
    print("✅ HF libraries imported")
except ImportError as e:
    print(f"❌ Failed to import: {e}")
    raise

# Initialize GLOBAL variables
hf_client = None
bertscore = None

if settings.HF_TOKEN:
    try:
        print("Initializing LLM Judge (Hugging Face hosted)...")
        hf_client = InferenceClient(
            model="meta-llama/Llama-3.1-8B-Instruct",
            token=settings.HF_TOKEN
        )
        print(f"✅ LLM Judge initialized: {hf_client is not None}")
    except Exception as e:
        print(f"❌ LLM Judge error: {e}")
        hf_client = None

    try:
        print("Initializing BERTScore...")
        bertscore = evaluate.load("bertscore")
        print(f"✅ BERTScore initialized: {bertscore is not None}")
    except Exception as e:
        print(f"❌ BERTScore error: {e}")
        bertscore = None
else:
    print(f"❌ HF_TOKEN not available")

print(f"\n{'='*70}")
print(f"MODULE LEVEL STATUS")
print(f"{'='*70}")
print(f"hf_client type: {type(hf_client)}")
print(f"hf_client is None: {hf_client is None}")
print(f"bertscore type: {type(bertscore)}")
print(f"bertscore is None: {bertscore is None}")
print(f"{'='*70}\n")

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

def evaluate_pipeline(pipeline_outputs: List[str], ground_truth: List[Dict]) -> Dict[str, Any]:
    """
    Evaluate pipelines using EXACT code from competition guide.
    """
    
    # ==========================================
    # CRITICAL: Check module-level globals
    # ==========================================
    import evaluation.evaluator as self_module
    
    print(f"\n{'='*70}")
    print(f"🔍 TOOL STATUS CHECK")
    print(f"{'='*70}")
    print(f"Module hf_client: {self_module.hf_client is not None} (type: {type(self_module.hf_client)})")
    print(f"Module bertscore: {self_module.bertscore is not None} (type: {type(self_module.bertscore)})")
    print(f"Local hf_client: {hf_client is not None}")
    print(f"Local bertscore: {bertscore is not None}")
    print(f"{'='*70}")
    
    # Use the module-level versions (most reliable)
    current_hf_client = self_module.hf_client
    current_bertscore = self_module.bertscore
    
    if current_hf_client is None or current_bertscore is None:
        print(f"❌ Tools not available!")
        print(f"   hf_client: {current_hf_client}")
        print(f"   bertscore: {current_bertscore}")
        
        # Try to re-initialize
        print(f"\n🔄 Attempting re-initialization...")
        try:
            if current_hf_client is None and settings.HF_TOKEN:
                self_module.hf_client = InferenceClient(
                    model="meta-llama/Llama-3.1-8B-Instruct",
                    token=settings.HF_TOKEN
                )
                print(f"   ✅ Re-initialized hf_client")
                current_hf_client = self_module.hf_client
        except Exception as e:
            print(f"   ❌ Re-init failed: {e}")
        
        if current_hf_client is None or current_bertscore is None:
            print(f"❌ Still not available after re-init attempt")
            return {
                "llm_judge_pass_rate": None,
                "bertscore_f1": None,
                "individual_judge_results": [None, None, None],
                "individual_bert_scores": [None, None, None],
            }
    
    if not pipeline_outputs or not ground_truth:
        print("❌ Empty inputs")
        return {
            "llm_judge_pass_rate": None,
            "bertscore_f1": None,
            "individual_judge_results": [],
            "individual_bert_scores": [],
        }
    
    try:
        print("\n" + "="*70)
        print("LLM-as-a-Judge Evaluation (Llama 3.1 8B hosted)")
        print("="*70)
        
        judge_results = []
        
        for i, (output, truth) in enumerate(zip(pipeline_outputs, ground_truth)):
            prompt = JUDGE_PROMPT.format(
                q=truth["question"],
                correct=truth["correct_answer"],
                answer=output
            )
            
            pipeline_name = ["Pipeline 1 (LLM Only)", "Pipeline 2 (RAG)", "Pipeline 3 (Multi-Agent)"][i]
            print(f"\n⏳ {pipeline_name}: Calling judge...")
            
            try:
                verdict = current_hf_client.chat_completion(
                    [{"role": "user", "content": prompt}],
                    max_tokens=10,
                    temperature=0.0
                )
                
                verdict_text = verdict.choices[0].message.content.strip().upper()
                result = "PASS" in verdict_text
                judge_results.append(result)
                
                print(f"   {pipeline_name}: {verdict_text} → {'✓ PASS' if result else '✗ FAIL'}")
            except Exception as e:
                print(f"   ❌ Judge error for {pipeline_name}: {e}")
                judge_results.append(None)
        
        if judge_results and any(r is not None for r in judge_results):
            valid_results = [r for r in judge_results if r is not None]
            judge_pass_rate = sum(valid_results) / len(valid_results)
            print(f"\n✅ LLM Judge Pass Rate: {judge_pass_rate:.1%}")
        else:
            judge_pass_rate = None
            print(f"\n⚠️  Judge evaluation had issues")
        
        # BERTScore (batch)
        print("\n" + "="*70)
        print("BERTScore Evaluation (rescaled 0-1)")
        print("="*70)
        
        try:
            print("⏳ Computing BERTScore...")
            bert_results = current_bertscore.compute(
                predictions=pipeline_outputs,
                references=[t["correct_answer"] for t in ground_truth],
                lang="en",
                rescale_with_baseline=True
            )
            
            bert_f1_scores = bert_results["f1"]
            for i, score in enumerate(bert_f1_scores):
                pipeline_name = ["Pipeline 1 (LLM Only)", "Pipeline 2 (RAG)", "Pipeline 3 (Multi-Agent)"][i]
                print(f"   {pipeline_name}: {score:.4f}")
            
            bertscore_f1_avg = sum(bert_f1_scores) / len(bert_f1_scores)
            print(f"\n✅ BERTScore F1 Average (rescaled): {bertscore_f1_avg:.4f}")
        except Exception as e:
            print(f"❌ BERTScore error: {e}")
            import traceback
            traceback.print_exc()
            bert_f1_scores = []
            bertscore_f1_avg = None
        
        print("="*70 + "\n")
        
        return {
            "llm_judge_pass_rate": round(judge_pass_rate, 4) if judge_pass_rate is not None else None,
            "bertscore_f1": round(bertscore_f1_avg, 4) if bertscore_f1_avg is not None else None,
            "individual_judge_results": judge_results,
            "individual_bert_scores": [round(s, 4) for s in bert_f1_scores] if bert_f1_scores else [],
        }
        
    except Exception as e:
        print(f"❌ Evaluation error: {e}")
        import traceback
        traceback.print_exc()
        return {
            "llm_judge_pass_rate": None,
            "bertscore_f1": None,
            "individual_judge_results": [],
            "individual_bert_scores": [],
        }

async def evaluate_pipeline_results(
    query: str,
    p1_answer: str,
    p2_answer: str,
    p3_answer: str
) -> Dict[str, Any]:
    """Legacy function for API compatibility"""
    
    print(f"\n{'='*70}")
    print(f"EVALUATION STARTED")
    print(f"{'='*70}")
    print(f"Query: {query}")
    
    # Load ground truth
    ground_truth_list = load_ground_truth()
    
    if not ground_truth_list:
        print("❌ No ground truth data available")
        return {
            "llm_judge_p1": None,
            "llm_judge_p2": None,
            "llm_judge_p3": None,
            "bertscore_p1": None,
            "bertscore_p2": None,
            "bertscore_p3": None,
        }
    
    # Find best matching ground truth
    best_match = find_best_match(query, ground_truth_list)
    
    if not best_match:
        print("❌ No matching ground truth found")
        return {
            "llm_judge_p1": None,
            "llm_judge_p2": None,
            "llm_judge_p3": None,
            "bertscore_p1": None,
            "bertscore_p2": None,
            "bertscore_p3": None,
        }
    
    print(f"✅ Using ground truth: {best_match['question']}")
    
    # Prepare ground truth for this query (same for all 3 pipelines)
    ground_truth = [best_match, best_match, best_match]
    pipeline_outputs = [p1_answer, p2_answer, p3_answer]
    
    # Evaluate using competition format
    results = evaluate_pipeline(pipeline_outputs, ground_truth)
    
    # Map results back to pipeline format
    individual_judge = results.get("individual_judge_results", [None, None, None])
    individual_bert = results.get("individual_bert_scores", [None, None, None])
    
    return {
        "llm_judge_p1": individual_judge[0] if len(individual_judge) > 0 else None,
        "llm_judge_p2": individual_judge[1] if len(individual_judge) > 1 else None,
        "llm_judge_p3": individual_judge[2] if len(individual_judge) > 2 else None,
        "bertscore_p1": individual_bert[0] if len(individual_bert) > 0 else None,
        "bertscore_p2": individual_bert[1] if len(individual_bert) > 1 else None,
        "bertscore_p3": individual_bert[2] if len(individual_bert) > 2 else None,
    }