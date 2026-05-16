# backend/pipelines/pipeline_3_orchestrator.py
"""
Pipeline 3: Multi-Agent Orchestrator
Coordinates Indexer → Filter → Historian agents
"""

import time
from typing import Dict, Any
from pipelines.agents import indexer, filter_agent, historian
import json


async def pipeline_3_orchestrator(query: str) -> dict:
    """
    Multi-Agent Pipeline:
    1. INDEXER: Queries TigerGraph Savanah
    2. FILTER: Ranks using centrality/pagerank
    3. HISTORIAN: Analyzes and explains findings
    """
    start_time = time.time()
    
    print("\n" + "="*70)
    print("🤖 PIPELINE 3: MULTI-AGENT ORCHESTRATOR")
    print("="*70)
    print(f"Query: {query}\n")
    
    try:
        # Step 1: INDEXER AGENT - Query TigerGraph
        print("Step 1: INDEXER AGENT - Querying TigerGraph Savanah")
        print("-" * 50)
        
        if "author" in query.lower():
            print("  📊 Fetching top authors...")
            raw_data = indexer.query_authors(limit=20)
            data_type = "authors"
        elif "paper" in query.lower() or "research" in query.lower():
            print("  📊 Running PageRank for top papers...")
            raw_data = indexer.query_papers(limit=20)
            data_type = "papers"
        else:
            print("  📊 Detecting research communities...")
            raw_data = indexer.query_papers(limit=15)
            data_type = "papers"
        
        if not raw_data:
            latency_ms = (time.time() - start_time) * 1000
            return {
                "answer": "❌ No data found in TigerGraph Savanah. Ensure TigerGraph connection is configured.",
                "latency_ms": round(latency_ms, 2),
                "tokens_in": 0,
                "tokens_out": 0,
                "tokens_total": 0,
                "sources": [],
                "cost": 0.0,
                "reasoning": "No data returned from TigerGraph INDEXER agent",
                "status": "error",
                "agents_used": ["INDEXER"]
            }
        
        # Step 2: FILTER AGENT - Rank and filter
        print("\nStep 2: FILTER AGENT - Ranking by centrality")
        print("-" * 50)
        
        ranked_data = filter_agent.rank_by_influence(raw_data)
        top_10 = ranked_data[:10]
        
        print(f"[FILTER] Ranked {len(ranked_data)} items, showing top 10")
        
        # Step 3: HISTORIAN AGENT - Analyze
        print("\nStep 3: HISTORIAN AGENT - AI Analysis")
        print("-" * 50)
        
        analysis = historian.analyze(top_10, query)
        
        latency_ms = (time.time() - start_time) * 1000
        
        print("\n" + "="*70)
        print(f"✅ Pipeline 3 Complete ({latency_ms:.0f}ms)")
        print("="*70 + "\n")
        
        # Extract source names
        sources = [
            item.get("title") or item.get("name") or str(item.get("id", ""))
            for item in top_10[:5]
        ]
        
        return {
            "answer": analysis,
            "latency_ms": round(latency_ms, 2),
            "tokens_in": 0,
            "tokens_out": 0,
            "tokens_total": 0,
            "sources": sources,
            "cost": 0.0,
            "reasoning": f"3-Agent Pipeline: INDEXER (TigerGraph) → FILTER (Ranking) → HISTORIAN (Analysis)",
            "status": "success",
            "agents_used": ["INDEXER", "FILTER", "HISTORIAN"],
            "indexer_memory": len(indexer.memory),
            "filter_memory": len(filter_agent.memory),
            "historian_history": len(historian.conversation_history)
        }
        
    except Exception as e:
        latency_ms = (time.time() - start_time) * 1000
        print(f"\n❌ Pipeline Error: {e}\n")
        import traceback
        traceback.print_exc()
        
        return {
            "answer": f"❌ Pipeline Error: {str(e)}\n\nEnsure TigerGraph Savanah connection is configured.",
            "latency_ms": round(latency_ms, 2),
            "tokens_in": 0,
            "tokens_out": 0,
            "tokens_total": 0,
            "sources": [],
            "cost": 0.0,
            "reasoning": f"Error in 3-Agent Pipeline: {str(e)}",
            "status": "error",
            "error": str(e)
        }