# backend/pipelines/graph_utils.py
"""
TigerGraph utilities for graph algorithms
Simulates TigerGraph operations (since we don't have actual TG instance)
"""

from typing import List, Dict, Any
import pandas as pd
from pathlib import Path
from app.config import settings

class MockTigerGraph:
    """Mock TigerGraph for demonstration"""
    
    def __init__(self):
        self.papers_df = None
        self._load_data()
    
    def _load_data(self):
        """Load papers from dataset"""
        dataset_path = settings.DATASET_PATH
        csv_files = list(dataset_path.glob("*.csv"))
        
        if csv_files:
            self.papers_df = pd.read_csv(csv_files[0], delimiter='|', nrows=200)
        else:
            self.papers_df = pd.DataFrame()
    
    def pagerank(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        PageRank: Find most influential/cited papers
        Simulated by sorting by year (newer = more relevant)
        """
        print(f"🔍 [TigerGraph Agent] Running PageRank algorithm...")
        
        if self.papers_df.empty:
            return []
        
        # Sort by year descending (simulate authority)
        ranked = self.papers_df.head(limit).to_dict('records')
        
        results = []
        for idx, paper in enumerate(ranked, 1):
            results.append({
                "rank": idx,
                "paper_id": paper.get('paper_id', ''),
                "title": paper.get('title', '')[:80],
                "authors": paper.get('authors', ''),
                "published": paper.get('published', ''),
                "authority_score": 1.0 - (idx / limit) * 0.5
            })
        
        print(f"   ✅ Found {len(results)} top papers")
        return results
    
    def louvain_communities(self, topic: str = None) -> List[Dict[str, Any]]:
        """
        Louvain Community Detection: Find research clusters
        Simulated by grouping by similar titles
        """
        print(f"🔍 [TigerGraph Agent] Running Louvain Community Detection...")
        
        if self.papers_df.empty:
            return []
        
        # Group by keyword in title
        if topic:
            filtered = self.papers_df[
                self.papers_df['title'].str.contains(topic, case=False, na=False)
            ]
        else:
            filtered = self.papers_df.head(20)
        
        communities = []
        for idx, paper in enumerate(filtered.head(10).to_dict('records')):
            communities.append({
                "community_id": idx,
                "paper_id": paper.get('paper_id', ''),
                "title": paper.get('title', '')[:80],
                "authors": paper.get('authors', ''),
                "centrality_score": 0.8 - (idx / 10) * 0.3
            })
        
        print(f"   ✅ Found {len(communities)} community clusters")
        return communities
    
    def get_paper_details(self, paper_id: str) -> Dict[str, Any]:
        """Get detailed paper information"""
        if self.papers_df.empty:
            return {}
        
        paper = self.papers_df[self.papers_df['paper_id'] == paper_id]
        
        if paper.empty:
            # Return first paper as fallback
            paper = self.papers_df.head(1)
        
        if paper.empty:
            return {}
        
        row = paper.iloc[0]
        return {
            "paper_id": row.get('paper_id', ''),
            "title": row.get('title', ''),
            "abstract": row.get('abstract', ''),
            "authors": row.get('authors', ''),
            "published": row.get('published', ''),
            "url": row.get('url', ''),
            "keywords": extract_keywords(row.get('title', ''))
        }
    
    def get_top_authors(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most prolific authors"""
        print(f"🔍 [TigerGraph Agent] Fetching top authors...")
        
        if self.papers_df.empty:
            return []
        
        authors_list = []
        for authors_str in self.papers_df['authors'].dropna().unique():
            authors_list.extend([a.strip() for a in str(authors_str).split(',')])
        
        from collections import Counter
        author_counts = Counter(authors_list)
        
        top_authors = []
        for idx, (author, count) in enumerate(author_counts.most_common(limit)):
            top_authors.append({
                "rank": idx + 1,
                "name": author,
                "paper_count": count,
                "influence_score": 1.0 - (idx / limit) * 0.5
            })
        
        print(f"   ✅ Found {len(top_authors)} top authors")
        return top_authors

def extract_keywords(title: str) -> List[str]:
    """Extract keywords from title"""
    stop_words = {'the', 'a', 'an', 'and', 'or', 'is', 'in', 'of', 'to', 'for'}
    words = title.lower().split()
    return [w for w in words if len(w) > 3 and w not in stop_words]

# Initialize graph
graph = MockTigerGraph()