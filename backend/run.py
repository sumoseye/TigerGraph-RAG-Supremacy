import uvicorn
import sys
from app.config import settings

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║     🚀 RESEARCH PIPELINE BATTLE - GROQ API EDITION 🚀           ║
║                                                                  ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  🌐 Backend: http://localhost:8000                              ║
║  📚 Docs:    http://localhost:8000/docs                         ║
║  🤖 Model:   Groq Llama 3.1                                     ║
║  💰 Cost:    $0.00 (FREE - 14,400 req/day)                      ║
║                                                                  ║
║  ✅ Pipeline 1: LLM Only (Ready)                                ║
║  ⏳ Pipeline 2: Basic RAG (Coming)                              ║
║  ⏳ Pipeline 3: TigerGraph (Coming)                             ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    try:
        uvicorn.run(
                "app.main:app",                    # ✅ Indented 4 more spaces
                host="0.0.0.0",
                port=8000,
                reload=True,
                timeout_keep_alive=300,
                limit_concurrency=10,
                timeout_graceful_shutdown=300
        )
    except KeyboardInterrupt:
        print("\n✅ Backend stopped")
        sys.exit(0)