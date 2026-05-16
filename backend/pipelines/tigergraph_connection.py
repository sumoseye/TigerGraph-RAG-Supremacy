# backend/pipelines/tigergraph_connection.py
"""
TigerGraph Savanah Connection Manager
Handles authentication and query execution
"""

import pyTigerGraph as tg
from app.config import settings
import json
from typing import List, Dict, Any

class TigerGraphSavanah:
    """Connect and interact with TigerGraph Savanah"""
    
    def __init__(self):
        self.conn = None
        self.token = None
        self._connect()
    
    def _connect(self):
        """Establish connection to TigerGraph Savanah"""
        try:
            print(f"\n🔌 Connecting to TigerGraph Savanah...")
            print(f"   Host: {settings.TIGERGRAPH_HOST}")
            print(f"   Graph: {settings.TIGERGRAPH_GRAPH_NAME}")
            
            # Create connection using pyTigerGraph
            self.conn = tg.TigerGraphConnection(
                host=settings.TIGERGRAPH_HOST,
                graphname=settings.TIGERGRAPH_GRAPH_NAME,
                gsqlSecret=settings.TIGERGRAPH_GSQL_SECRET,
                restppPort=settings.TIGERGRAPH_REST_PORT,
                gsPort=settings.TIGERGRAPH_GS_PORT,
            )
            
            # Get authentication token
            print(f"   🔑 Authenticating...")
            self.token = self.conn.getToken(settings.TIGERGRAPH_GSQL_SECRET)
            
            # Test connection
            version = self.conn.getVersion()
            print(f"   ✅ Connected! TigerGraph Version: {version}\n")
            
        except Exception as e:
            print(f"   ❌ Connection failed: {e}")
            print(f"   Check TIGERGRAPH credentials in .env\n")
            self.conn = None
    
    def get_vertices(self, vertex_type: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get vertices of a specific type"""
        if not self.conn:
            return []
        
        try:
            print(f"   📊 Fetching {vertex_type} vertices...")
            vertices = self.conn.getVertices(vertex_type, limit=limit)
            print(f"   ✅ Got {len(vertices)} vertices")
            return vertices
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return []
    
    def run_gsql_query(self, query: str) -> Any:
        """Run GSQL query"""
        if not self.conn:
            return None
        
        try:
            print(f"   🔍 Running GSQL query...")
            result = self.conn.gsql(query)
            print(f"   ✅ Query executed")
            return result
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return None
    
    def run_installed_query(self, query_name: str, params: Dict = None) -> Any:
        """Run pre-installed query from Savanah"""
        if not self.conn:
            return None
        
        try:
            print(f"   🚀 Running installed query: {query_name}")
            result = self.conn.runInstalledQuery(query_name, params or {})
            print(f"   ✅ Query executed")
            return result
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return None
    
    def get_vertex_stats(self) -> Dict[str, int]:
        """Get statistics about vertices"""
        if not self.conn:
            return {}
        
        try:
            stats = self.conn.getVertexCount("*")
            return stats
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return {}
    
    def get_edges(self, source_vertex: str, edge_type: str = None, limit: int = 100) -> List[Dict]:
        """Get edges connected to a vertex"""
        if not self.conn:
            return []
        
        try:
            edges = self.conn.getEdges(source_vertex, edgeType=edge_type, limit=limit)
            return edges
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return []


# Initialize global instance
try:
    tg_savanah = TigerGraphSavanah()
except Exception as e:
    print(f"❌ Failed to initialize TigerGraph: {e}")
    tg_savanah = None