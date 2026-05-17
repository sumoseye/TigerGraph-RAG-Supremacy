# backend/pipelines/pipeline_2_rag.py
import time
from pathlib import Path
import pandas as pd
from typing import Dict, Any, List
import chromadb
from groq import Groq
from app.config import settings

# Initialize Groq
groq_client = Groq(api_key=settings.GROQ_API_KEY)

# Initialize ChromaDB
chroma_client = chromadb.EphemeralClient()

# Global collection cache
_collection = None

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

def get_or_create_collection():
    """Get or create ChromaDB collection"""
    global _collection
    
    if _collection is not None:
        return _collection
    
    print(f"\n{'='*70}")
    print(f"CREATING CHROMADB COLLECTION")
    print(f"{'='*70}")
    
    # Delete existing collection if it exists
    try:
        chroma_client.delete_collection(name="arxiv_papers")
    except:
        pass
    
    # Create new collection
    _collection = chroma_client.create_collection(
        name="arxiv_papers",
        metadata={"hnsw:space": "cosine"}
    )
    
    print(f"Collection created\n")
    return _collection

def index_dataset() -> Dict[str, Any]:
    """Index arXiv dataset into ChromaDB"""
    dataset_path = settings.DATASET_PATH
    
    print(f"\n{'='*70}")
    print(f"INDEXING DATASET INTO CHROMADB")
    print(f"{'='*70}")
    
    if not dataset_path.exists():
        return {"indexed": 0, "collection_size": 0}
    
    collection = get_or_create_collection()
    
    csv_files = list(dataset_path.glob("*.csv"))
    
    if not csv_files:
        print("No CSV files found")
        return {"indexed": 0, "collection_size": 0}
    
    csv_file = csv_files[0]
    print(f"Reading: {csv_file.name}")
    
    try:
        # Read CSV with pipe delimiter
        df = pd.read_csv(csv_file, delimiter='|', nrows=500)  # Index 500 papers
        print(f"Loaded {len(df)} papers")
        
        # Prepare data for ChromaDB
        documents = []
        metadatas = []
        ids = []
        
        for idx, row in df.iterrows():
            try:
                # Combine title + abstract for better search
                doc_text = f"Title: {row['title']}\n\nAbstract: {row['abstract']}"
                
                documents.append(doc_text)
                
                metadatas.append({
                    "title": str(row['title'])[:100],
                    "authors": str(row['authors'])[:100],
                    "published": str(row['published'])[:20],
                    "paper_id": str(row['paper_id'])
                })
                
                ids.append(f"paper_{idx}")
                
            except Exception as e:
                print(f"  Warning - Error processing row {idx}: {e}")
                continue
        
        # Add to collection
        if documents:
            print(f"\nAdding {len(documents)} papers to ChromaDB...")
            collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            print(f"Indexed {len(documents)} papers")
        
        print(f"\n{'='*70}")
        print(f"ChromaDB Collection Size: {collection.count()}")
        print(f"{'='*70}\n")
        
        return {
            "indexed": len(documents),
            "collection_size": collection.count()
        }
        
    except Exception as e:
        print(f"Error indexing: {e}")
        import traceback
        traceback.print_exc()
        return {"indexed": 0, "collection_size": 0}

def search_papers(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """Search papers in ChromaDB"""
    collection = get_or_create_collection()
    
    # If collection is empty, index first
    if collection.count() == 0:
        print("Collection empty, indexing now...")
        index_dataset()
    
    print(f"\nSearching for: '{query}'")
    
    try:
        # Query ChromaDB
        results = collection.query(
            query_texts=[query],
            n_results=top_k
        )
        
        papers = []
        if results and results['documents']:
            for i, doc in enumerate(results['documents'][0]):
                papers.append({
                    "content": doc,
                    "metadata": results['metadatas'][0][i] if results['metadatas'] else {},
                    "distance": results['distances'][0][i] if results['distances'] else 0
                })
        
        print(f"Found {len(papers)} relevant papers")
        return papers
        
    except Exception as e:
        print(f"Search error: {e}")
        return []

async def pipeline_2_rag(query: str) -> dict:
    """Pipeline 2: Basic RAG with ChromaDB + Groq"""
    start_time = time.time()
    
    try:
        print(f"\n{'='*70}")
        print(f"PIPELINE 2: BASIC RAG")
        print(f"{'='*70}")
        print(f"Query: {query}\n")
        
        # Step 1: Search for relevant papers
        print("Step 1: Vector Search")
        relevant_papers = search_papers(query, top_k=5)
        
        if not relevant_papers:
            return {
                "answer": "No relevant papers found in dataset",
                "latency_ms": (time.time() - start_time) * 1000,
                "tokens_in": 0,
                "tokens_out": 0,
                "tokens_total": 0,
                "sources": [],
                "cost": 0.0,
                "reasoning": "RAG search returned 0 results",
                "status": "error",
                "retrieval_count": 0
            }
        
        # Step 2: Build context from retrieved papers
        print(f"\nStep 2: Building Context from {len(relevant_papers)} papers")
        context = "Retrieved Papers:\n\n"
        sources = []
        
        seen_titles = set()
        for i, paper in enumerate(relevant_papers, 1):
            context += f"Paper {i}:\n"
            context += f"{paper['content'][:500]}...\n"
            context += f"Author: {paper['metadata'].get('authors', 'Unknown')}\n"
            context += f"Published: {paper['metadata'].get('published', 'Unknown')}\n"
            context += "-" * 50 + "\n\n"
            
            title = paper['metadata'].get('title', '')
            if title and title not in seen_titles:
                sources.append(title)
                seen_titles.add(title)
        
        # Step 3: Generate answer with Groq
        print(f"\nStep 3: Generating Answer with Groq")
        
        system_prompt = """You are an expert research assistant using Retrieval-Augmented Generation (RAG).
You have retrieved the most relevant papers from an arXiv database based on the user's query.
Use the retrieved papers to provide a comprehensive, accurate answer.
Do NOT use markdown formatting, asterisks, bold text, or special characters.
Use plain text only and cite which papers you reference."""
        
        user_prompt = f"""Retrieved Context:
{context}

---
User Query: {query}

Based on the papers above, provide a detailed answer in plain text:"""
        
        print(f"Calling Groq API...")
        
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
        
        print(f"Response in {latency_ms:.0f}ms\n")
        
        return {
            "answer": answer,
            "latency_ms": round(latency_ms, 2),
            "tokens_in": response.usage.prompt_tokens,
            "tokens_out": response.usage.completion_tokens,
            "tokens_total": response.usage.total_tokens,
            "sources": sources,
            "cost": 0.0,
            "reasoning": f"RAG Pipeline: Vector Search (5 papers) + Groq Generation",
            "status": "success",
            "retrieval_count": len(relevant_papers)
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
            "error": str(e),
            "retrieval_count": 0
        }