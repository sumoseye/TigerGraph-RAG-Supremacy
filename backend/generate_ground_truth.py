# backend/generate_ground_truth.py
"""
Run queries through Pipeline 3 (GraphRAG) and save outputs as ground truth.
Uses temperature=0 for consistent outputs.
"""

import asyncio
import json
from pathlib import Path
from groq import Groq
from app.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)

QUERIES = [
    "What is MetaFormer?",
    "What are neural network architectures?",
    "How do autoencoders work?",
    "What is federated learning?",
    "What are graph neural networks?",
    "How is machine learning used in physics?",
    "What are the applications of deep learning in healthcare?",
    "What is reinforcement learning?",
    "How do attention mechanisms work?",
    "What are reconfigurable robots?",
    "What is time series outlier detection?",
    "How does edge computing work?",
    "What are the challenges in quantum computing?",
    "How do language models work?",
    "What are transformers in machine learning?",
]

async def generate_answer(query: str) -> str:
    """Generate answer with temperature=0 for consistency"""
    
    prompt = f"""You are an expert AI researcher. Answer this question in 3-4 detailed sentences, including specific technical terms, architectures, and applications.

Question: {query}

Provide a comprehensive technical answer:"""
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,  # ← Deterministic output
        max_tokens=300
    )
    
    return response.choices[0].message.content.strip()

async def generate_ground_truth():
    """Generate ground truth answers"""
    
    print("="*70)
    print("GENERATING GROUND TRUTH (Temperature=0)")
    print("="*70)
    
    ground_truth = []
    
    for i, query in enumerate(QUERIES, 1):
        print(f"\n[{i}/{len(QUERIES)}] Query: {query}")
        print("-" * 70)
        
        try:
            answer = await generate_answer(query)
            
            print(f"✅ Got answer ({len(answer)} chars)")
            print(f"Preview: {answer[:150]}...")
            
            ground_truth.append({
                "question": query,
                "correct_answer": answer
            })
            
            await asyncio.sleep(1)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            continue
    
    # Save
    output_path = Path(__file__).parent / "evaluation" / "ground_truth.json"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(ground_truth, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*70)
    print(f"✅ SAVED {len(ground_truth)} ANSWERS")
    print(f"📁 {output_path}")
    print("="*70)

if __name__ == "__main__":
    asyncio.run(generate_ground_truth())