# backend/test_schema.py
from pipelines.tigergraph_connection import tg_savanah

print("\n🔍 Checking TigerGraph Schema...\n")

if tg_savanah and tg_savanah.conn:
    # Get vertex types
    try:
        schema = tg_savanah.conn.getSchema()
        print("📊 Vertex Types in Your Graph:")
        for vertex_type in schema.get("VertexTypes", []):
            print(f"  - {vertex_type['Name']}")
        
        print("\n🔗 Edge Types in Your Graph:")
        for edge_type in schema.get("EdgeTypes", []):
            print(f"  - {edge_type['Name']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        
        # Alternative: Try getting vertex counts
        try:
            stats = tg_savanah.get_vertex_stats()
            print("\n📊 Vertex Counts:")
            for vertex_type, count in stats.items():
                print(f"  - {vertex_type}: {count} vertices")
        except Exception as e2:
            print(f"❌ Error: {e2}")
else:
    print("❌ No TigerGraph connection")