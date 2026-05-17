# backend/pipelines/pipeline_1_llm_only.py
import time
from pathlib import Path
import json
import pandas as pd
from typing import Dict, Any
from groq import Groq
from app.config import settings

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

def load_dataset() -> Dict[str, Any]:
    """Load dataset - handles pipe-delimited CSV"""
    dataset_path = settings.DATASET_PATH
    
    print(f"\n{'='*70}")
    print(f"LOADING DATASET")
    print(f"{'='*70}")
    print(f"Path: {dataset_path}")
    
    if not dataset_path.exists():
        print(f"Dataset folder not found!")
        return {"content": "No dataset available.", "files": []}
    
    documents = []
    file_list = []
    
    print(f"\nScanning for CSV files...")
    
    csv_files = list(dataset_path.glob("*.csv"))
    print(f"Found {len(csv_files)} CSV files")
    
    for csv_file in csv_files:
        try:
            print(f"\n  {csv_file.name}")
            file_size_mb = csv_file.stat().st_size / (1024 * 1024)
            print(f"     Size: {file_size_mb:.1f} MB")
            
            # READ WITH PIPE DELIMITER (|)
            print(f"     Reading first 150 rows (pipe-delimited)...")
            df = pd.read_csv(csv_file, delimiter='|', nrows=150)
            
            print(f"     Loaded {len(df)} rows, {len(df.columns)} columns")
            print(f"     Columns: {list(df.columns)}")
            
            file_list.append(csv_file.name)
            
            # Format for LLM
            csv_text = f"ARXIV DATASET: {csv_file.name}\n"
            csv_text += f"File Size: {file_size_mb:.1f} MB\n"
            csv_text += f"Total Records: 44,490\n"
            csv_text += f"Showing: First 150 records\n"
            csv_text += f"Columns: {', '.join(df.columns)}\n"
            csv_text += "---\nSample Data:\n"
            csv_text += df.to_string()
            
            documents.append(csv_text)
            print(f"     Formatted ({len(csv_text)} chars)")
            
        except Exception as e:
            print(f"     Error: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    full_content = "\n\n".join(documents) if documents else "NO DATA LOADED"
    
    # Limit for LLM context
    max_chars = 15000
    if len(full_content) > max_chars:
        full_content = full_content[:max_chars] + "\n\n[... remaining records truncated ...]"
    
    print(f"\n{'='*70}")
    print(f"Files loaded: {file_list}")
    print(f"Content size: {len(full_content)} characters")
    print(f"{'='*70}\n")
    
    return {"content": full_content, "files": file_list}

async def pipeline_1_llm_only(query: str) -> dict:
    """Pipeline 1: Groq LLM with arXiv dataset"""
    start_time = time.time()
    
    try:
        print(f"\n{'='*70}")
        print(f"PIPELINE 1: LLM ONLY")
        print(f"{'='*70}")
        print(f"Query: {query}\n")
        
        dataset = load_dataset()
        context = dataset["content"]
        
        print(f"Context: {len(context)} chars from {dataset['files']}")
        
        system_prompt = """You are an expert AI researcher analyzing arXiv papers.
You have access to a sample of arXiv research papers with titles, abstracts, authors, and publication dates.
Answer questions about these papers based on the data provided.
Do NOT use markdown formatting, asterisks, bold text, or special characters.
Use plain text only. Be specific and cite paper titles when relevant."""
        
        user_prompt = f"""ArXiv Research Dataset:
{context}

---
User Question: {query}

Based on the papers in this dataset, provide a detailed answer in plain text:"""
        
        print(f"Calling Groq API ({len(user_prompt)} chars)...")
        
        response = groq_client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=1024
        )
        
        answer = response.choices[0].message.content
        answer = clean_markdown(answer)  # Remove any markdown
        latency_ms = (time.time() - start_time) * 1000
        
        print(f"Response in {latency_ms:.0f}ms")
        print(f"Tokens: {response.usage.total_tokens}\n")
        
        return {
            "answer": answer,
            "latency_ms": round(latency_ms, 2),
            "tokens_in": response.usage.prompt_tokens,
            "tokens_out": response.usage.completion_tokens,
            "tokens_total": response.usage.total_tokens,
            "sources": dataset["files"],
            "cost": 0.0,
            "reasoning": f"Groq {settings.GROQ_MODEL} with arXiv dataset sample",
            "status": "success"
        }
        
    except Exception as e:
        latency_ms = (time.time() - start_time) * 1000
        print(f"Error: {e}\n")
        
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