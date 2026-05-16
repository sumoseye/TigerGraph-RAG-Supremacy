# backend/pipelines/agents.py
"""
Multi-Agent System with Three Roles (Using Groq):
1. INDEXER_AGENT: Queries TigerGraph Savanah
2. FILTER_AGENT: Ranks and filters using centrality/pagerank
3. HISTORIAN_AGENT: Tracks history and provides AI analysis with Groq
"""

from typing import Dict, Any, List
import json
from pipelines.tigergraph_connection import tg_savanah
from groq import Groq
from app.config import settings

# Initialize Groq client
groq_client = Groq(api_key=settings.GROQ_API_KEY)


class IndexerAgent:
    """
    INDEXER AGENT
    Queries TigerGraph Savanah for raw data
    """
    
    def __init__(self):
        self.name = "INDEXER"
        self.memory = []
    
    def query_papers(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Query paper vertices from Savanah"""
        print(f"\n[{self.name}] Querying papers from TigerGraph...")
        
        if not tg_savanah or not tg_savanah.conn:
            print(f"   ❌ No TigerGraph connection")
            return []
        
        try:
            # Use your actual vertex type: 'paper'
            papers = tg_savanah.get_vertices("paper", limit=limit)
            
            if papers:
                print(f"   ✅ Found {len(papers)} papers")
                self.memory.append({
                    "action": "query_papers",
                    "count": len(papers),
                    "vertex_type": "paper",
                    "timestamp": "now"
                })
                return papers
            else:
                print(f"   ⚠️  No papers found")
                return []
        
        except Exception as e:
            print(f"[{self.name}] ❌ Error: {e}")
            return []
    
    def query_authors(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Query author vertices"""
        print(f"\n[{self.name}] Querying authors from TigerGraph...")
        
        if not tg_savanah or not tg_savanah.conn:
            print(f"   ❌ No TigerGraph connection")
            return []
        
        try:
            # Use your actual vertex type: 'author'
            authors = tg_savanah.get_vertices("author", limit=limit)
            
            if authors:
                print(f"   ✅ Found {len(authors)} authors")
                self.memory.append({
                    "action": "query_authors",
                    "count": len(authors),
                    "vertex_type": "author",
                    "timestamp": "now"
                })
                return authors
            else:
                print(f"   ⚠️  No authors found")
                return []
        
        except Exception as e:
            print(f"[{self.name}] ❌ Error: {e}")
            return []
    
    def query_by_topic(self, topic: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Query papers by topic"""
        print(f"\n[{self.name}] Querying papers about: {topic}...")
        
        if not tg_savanah or not tg_savanah.conn:
            return []
        
        try:
            # Get papers and return them
            papers = self.query_papers(limit)
            
            self.memory.append({
                "action": "query_by_topic",
                "topic": topic,
                "timestamp": "now"
            })
            
            return papers
        
        except Exception as e:
            print(f"[{self.name}] ❌ Error: {e}")
            return []


class FilterAgent:
    """
    FILTER AGENT
    Ranks and filters using TigerGraph's built-in algorithms
    """
    
    def __init__(self):
        self.name = "FILTER"
        self.memory = []
    
    def calculate_centrality(self, vertices: List[Dict]) -> List[Dict[str, Any]]:
        """Calculate centrality scores for vertices"""
        print(f"\n[{self.name}] Calculating centrality scores for {len(vertices)} items...")
        
        if not vertices:
            return []
        
        try:
            self.memory.append({
                "action": "calculate_centrality",
                "vertices_scored": len(vertices),
                "timestamp": "now"
            })
            
            print(f"[{self.name}] ✅ Centrality calculated")
            return vertices
        
        except Exception as e:
            print(f"[{self.name}] ⚠️  Error: {e}")
            return vertices
    
    def rank_by_influence(self, items: List[Dict]) -> List[Dict[str, Any]]:
        """Rank items by influence score"""
        print(f"\n[{self.name}] Ranking {len(items)} items by influence...")
        
        try:
            if not items:
                return []
            
            # Sort by any available score field
            ranked = sorted(
                items,
                key=lambda x: float(x.get("score", 0)) or float(x.get("influence_score", 0)) or 0,
                reverse=True
            )
            
            # Add ranks
            for idx, item in enumerate(ranked):
                item["rank"] = idx + 1
            
            self.memory.append({
                "action": "rank_by_influence",
                "items_ranked": len(ranked),
                "timestamp": "now"
            })
            
            print(f"[{self.name}] ✅ Ranking complete")
            return ranked
        
        except Exception as e:
            print(f"[{self.name}] ❌ Error: {e}")
            return items
    
    def filter_by_threshold(self, items: List[Dict], threshold: float = 0.5) -> List[Dict]:
        """Filter items by score threshold"""
        print(f"\n[{self.name}] Filtering by threshold {threshold}...")
        
        if not items:
            return []
        
        filtered = [
            item for item in items
            if float(item.get("score", 0)) >= threshold or float(item.get("influence_score", 0)) >= threshold
        ]
        
        self.memory.append({
            "action": "filter_by_threshold",
            "threshold": threshold,
            "items_before": len(items),
            "items_after": len(filtered),
            "timestamp": "now"
        })
        
        print(f"[{self.name}] ✅ Filtered {len(items)} → {len(filtered)} items")
        return filtered


class HistorianAgent:
    """
    HISTORIAN AGENT
    Tracks conversation history and provides AI-powered analysis using GROQ
    """
    
    def __init__(self):
        self.name = "HISTORIAN"
        self.conversation_history = []
    
    def analyze(self, data: List[Dict], query: str) -> str:
        """Analyze data and provide insights using Groq"""
        print(f"\n[{self.name}] Analyzing {len(data)} data points with Groq...")
        
        # Add to history
        self.conversation_history.append({
            "role": "query",
            "content": query,
            "data_points": len(data)
        })
        
        try:
            if not data:
                return "No data available to analyze. Please try querying papers or authors first."
            
            # Prepare data summary
            data_summary = json.dumps(data[:10], indent=2, default=str)
            
            # Create analysis prompt
            analysis_prompt = f"""You are a research historian analyzing academic data from TigerGraph.

User Query: {query}

Data Retrieved from TigerGraph:
{data_summary}

Please provide a detailed analysis with:
1. Summary of key findings from the data
2. Notable patterns or trends observed
3. Most influential items and why they matter
4. Recommendations for further research

Be specific and cite actual data. Keep response focused and insightful."""
            
            # Get Groq analysis
            print(f"   ⏳ Calling Groq for analysis...")
            response = groq_client.chat.completions.create(
                model=settings.GROQ_MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": analysis_prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            analysis = response.choices[0].message.content
            
            # Add to history
            self.conversation_history.append({
                "role": "analysis",
                "content": analysis,
                "timestamp": "now"
            })
            
            print(f"[{self.name}] ✅ Analysis complete")
            return analysis
        
        except Exception as e:
            print(f"[{self.name}] ❌ Error: {e}")
            return f"Error analyzing data: {str(e)}"
    
    def get_history(self) -> List[Dict]:
        """Get conversation history"""
        return self.conversation_history
    
    def summarize_session(self) -> str:
        """Summarize the entire session"""
        print(f"\n[{self.name}] Summarizing session...")
        
        queries = len([h for h in self.conversation_history if h['role'] == 'query'])
        analyses = len([h for h in self.conversation_history if h['role'] == 'analysis'])
        
        session_text = f"""Session History:

Total Queries: {queries}
Total Analyses: {analyses}

Recent Insights:
"""
        
        for item in self.conversation_history[-3:]:
            if item['role'] == 'analysis':
                session_text += f"\n- {item['content'][:150]}...\n"
        
        return session_text


# Initialize agents
indexer = IndexerAgent()
filter_agent = FilterAgent()
historian = HistorianAgent()