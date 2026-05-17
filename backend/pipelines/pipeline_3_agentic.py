# backend/pipelines/pipeline_3_agentic.py
import time
from typing import Dict, Any, List
from groq import Groq
from app.config import settings
import json

# Initialize Groq
groq_client = Groq(api_key=settings.GROQ_API_KEY)

def clean_markdown(text: str) -> str:
    """Remove markdown formatting from text"""
    text = text.replace('**', '')
    text = text.replace('*', '')
    text = text.replace('_', '')
    text = text.replace('`', '')
    text = text.replace('##', '')
    text = text.replace('#', '')
    import re
    text = re.sub(r'^\s*[-•]\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\d+\.\s+', '', text, flags=re.MULTILINE)
    return text.strip()

async def pipeline_3_agentic(query: str) -> dict:
    """
    Pipeline 3: Advanced Reasoning with Groq
    Uses multi-turn analysis for deeper research insights
    """
    start_time = time.time()
    
    print(f"\n{'='*70}")
    print(f"PIPELINE 3: ADVANCED ANALYSIS")
    print(f"{'='*70}")
    print(f"Query: {query}\n")
    
    try:
        system_prompt = """You are an advanced AI research analyst.
Provide deep, analytical insights about research topics.
Do NOT use markdown formatting, asterisks, bold text, or special characters.
Use plain text only. Explain your reasoning step-by-step.
Synthesize information to provide comprehensive answers."""

        user_prompt = f"""Analyze this research question comprehensively:

Query: {query}

Provide:
1. Overview of the topic
2. Key research areas
3. Current trends and developments
4. Future directions
5. Practical applications

Use plain text, no markdown formatting:"""
        
        print(f"Calling Groq API for advanced analysis...")
        
        response = groq_client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.8,
            max_tokens=1024
        )
        
        answer = response.choices[0].message.content
        answer = clean_markdown(answer)  # Remove any markdown
        latency_ms = (time.time() - start_time) * 1000
        
        print(f"Response in {latency_ms:.0f}ms\n")
        
        return {
            "answer": answer,
            "latency_ms": round(latency_ms, 2),
            "tokens_in": response.usage.prompt_tokens,
            "tokens_out": response.usage.completion_tokens,
            "tokens_total": response.usage.total_tokens,
            "sources": ["Advanced Analysis"],
            "cost": 0.0,
            "reasoning": f"Groq {settings.GROQ_MODEL} with advanced multi-step reasoning",
            "status": "success",
            "turns": 1
        }
        
    except Exception as e:
        latency_ms = (time.time() - start_time) * 1000
        print(f"Error: {e}\n")
        import traceback
        traceback.print_exc()
        
        return {
            "answer": f"Error: {str(e)}",
            "latency_ms": round(latency_ms, 2),
            "tokens_in": 0,
            "tokens_out": 0,
            "tokens_total": 0,
            "sources": [],
            "cost": 0.0,
            "reasoning": f"Error: {str(e)}",
            "status": "error",
            "error": str(e)
        }