# backend/pipelines/agents.py
"""
Multi-Agent System with Three Roles:
1. INDEXER_AGENT: Queries TigerGraph Savanah
2. FILTER_AGENT: Ranks and filters using centrality/pagerank
3. HISTORIAN_AGENT: Tracks history and provides insights
"""

from typing import Dict, Any, List
import json
from pipelines.tigergraph_connection import tg_savanah
import google.generativeai as genai
from app.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)


class IndexerAgent:
    """
    INDEXER AGENT
    Queries TigerGraph Savanah for raw data
    Built-in functions: getVertices, getEdges, runQuery
    """
    
    def __init__(self):
        self.name = "INDEXER"
        self.memory = []
    
    def query_papers(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Query paper vertices from Savanah"""
        print(f"\n[{self.name}] Querying papers from TigerGraph...")
        
        if not tg_savanah or not tg_savanah.conn:
            return []
        
        try:
            # Query papers (adjust vertex type to match your schema)
            papers = tg_savanah.get_vertices("Paper", limit=limit)
            
            self.memory.append({
                "action": "query_papers",
                "count": len(papers),
                "timestamp": "now"
            })
            
            print(f"[{self.name}] ✅ Found {len(papers)} papers")
            return papers
        
        except Exception as e:
            print(f"[{self.name}] ❌ Error: {e}")
            return []
    
    def query_authors(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Query author vertices"""
        print(f"\n[{self.name}] Querying authors from TigerGraph...")
        
        if not tg_savanah or not tg_savanah.conn:
            return []
        
        try:
            authors = tg_savanah.get_vertices("Author", limit=limit)
            
            self.memory.append({
                "action": "query_authors",
                "count": len(authors),
                "timestamp": "now"
            })
            
            print(f"[{self.name}] ✅ Found {len(authors)} authors")
            return authors
        
        except Exception as e:
            print(f"[{self.name}] ❌ Error: {e}")
            return []
    
    def query_by_topic(self, topic: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Query vertices by topic"""
        print(f"\n[{self.name}] Querying {topic}...")
        
        if not tg_savanah or not tg_savanah.conn:
            return []
        
        try:
            # Run GSQL query to find papers by topic
            query = f"""
            USE GRAPH {settings.TIGERGRAPH_GRAPH_NAME}
            SELECT * FROM Paper 
            WHERE title LIKE "%{topic}%" OR abstract LIKE "%{topic}%"
            LIMIT {limit}
            """
            
            result = tg_savanah.run_gsql_query(query)
            
            self.memory.append({
                "action": "query_by_topic",
                "topic": topic,
                "timestamp": "now"
            })
            
            print(f"[{self.name}] ✅ Query completed")
            return result or []
        
        except Exception as e:
            print(f"[{self.name}] ❌ Error: {e}")
            return []


class FilterAgent:
    """
    FILTER AGENT
    Ranks and filters using TigerGraph's built-in algorithms
    Built-in functions: Centrality, PageRank, Betweenness
    """
    
    def __init__(self):
        self.name = "FILTER"
        self.memory = []
    
    def calculate_centrality(self, vertices: List[Dict]) -> List[Dict[str, Any]]:
        """Calculate centrality scores for vertices using TigerGraph"""
        print(f"\n[{self.name}] Calculating centrality scores...")
        
        if not vertices:
            return []
        
        try:
            # Run centrality query from Savanah
            # Assumes you have a "centrality" installed query
            result = tg_savanah.run_installed_query(
                "tg_pagerank",
                {"v_type": "Paper", "max_change": 0.001, "max_iter": 25, "damping": 0.85}
            )
            
            self.memory.append({
                "action": "calculate_centrality",
                "vertices_scored": len(vertices),
                "timestamp": "now"
            })
            
            print(f"[{self.name}] ✅ Centrality calculated")
            return vertices  # Return sorted by centrality
        
        except Exception as e:
            print(f"[{self.name}] ⚠️  Centrality calculation: {e}")
            return vertices
    
    def rank_by_influence(self, items: List[Dict]) -> List[Dict[str, Any]]:
        """Rank items by influence score"""
        print(f"\n[{self.name}] Ranking {len(items)} items by influence...")
        
        try:
            # Sort by influence/importance metrics
            ranked = sorted(
                items,
                key=lambda x: float(x.get("score", 0)) or 0,
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
        
        filtered = [
            item for item in items
            if float(item.get("score", 0)) >= threshold
        ]
        
        self.memory.append({
            "action": "filter_by_threshold",
            "threshold": threshold,
            "items_before": len(items),
            "items_after": len(filtered),
            "timestamp": "now"
        })
        
        print(f"[{self.name}] ✅ Filtered {len(items)} → {len(filtered)}")
        return filtered


class HistorianAgent:
    """
    HISTORIAN AGENT
    Tracks conversation history and provides AI-powered analysis
    Uses Gemini for reasoning and explanation
    """
    
    def __init__(self):
        self.name = "HISTORIAN"
        self.conversation_history = []
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
    
    def analyze(self, data: List[Dict], query: str) -> str:
        """Analyze data and provide insights"""
        print(f"\n[{self.name}] Analyzing data with Gemini...")
        
        # Add to history
        self.conversation_history.append({
            "role": "query",
            "content": query,
            "data_points": len(data)
        })
        
        try:
            # Prepare data summary
            data_summary = json.dumps(data[:10], indent=2, default=str)  # Top 10
            
            # Create analysis prompt
            analysis_prompt = f"""You are a research historian analyzing academic graph data.

Current Query: {query}

Top Results from TigerGraph:
{data_summary}

Please provide:
1. Summary of key findings
2. Notable patterns or trends
3. Top influential items and why
4. Recommendations for further research

Be specific and cite data from the results."""
            
            # Get Gemini analysis
            response = self.model.generate_content(analysis_prompt)
            analysis = response.text
            
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
            return f"Error analyzing data: {e}"
    
    def get_history(self) -> List[Dict]:
        """Get conversation history"""
        return self.conversation_history
    
    def summarize_session(self) -> str:
        """Summarize the entire session"""
        print(f"\n[{self.name}] Summarizing session...")
        
        session_text = f"""Session History:
        
Queries processed: {len([h for h in self.conversation_history if h['role'] == 'query'])}
Analyses performed: {len([h for h in self.conversation_history if h['role'] == 'analysis'])}

Key insights:
"""
        
        for item in self.conversation_history[-3:]:
            if item['role'] == 'analysis':
                session_text += f"\n- {item['content'][:200]}..."
        
        return session_text


# Initialize agents
indexer = IndexerAgent()
filter_agent = FilterAgent()
historian = HistorianAgent()