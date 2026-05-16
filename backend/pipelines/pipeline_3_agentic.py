# backend/pipelines/pipeline_3_agentic.py
"""
Pipeline 3: Agentic Multimodal Researcher
Uses Mistral with tool use (function calling) to orchestrate:
- TigerGraph algorithms (PageRank, Louvain)
- PDF extraction with vision analysis
- Multi-turn reasoning with chain-of-thought
"""

import time
from typing import Dict, Any, List
from mistralai import Mistral
from app.config import settings
from pipelines.graph_utils import graph
from pipelines.pdf_utils import extract_images_from_pdf
import json

# Initialize Mistral client
mistral_client = Mistral(api_key=settings.GROQ_API_KEY.replace("gsk_", "sk_") if "gsk_" in settings.GROQ_API_KEY else settings.GROQ_API_KEY)

# Agent roles
INDEXER_AGENT = "INDEXER"  # Finds data in graph
FILTER_AGENT = "FILTER"    # Ranks and filters results
HISTORIAN_AGENT = "HISTORIAN"  # Analyzes and explains

def define_tools() -> List[Dict[str, Any]]:
    """Define available tools for Mistral"""
    return [
        {
            "type": "function",
            "function": {
                "name": "pagerank_algorithm",
                "description": "Find most influential/authoritative papers using PageRank",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "limit": {
                            "type": "integer",
                            "description": "Number of top papers to return (default 10)"
                        }
                    }
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "louvain_communities",
                "description": "Discover research communities/clusters using Louvain algorithm",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "topic": {
                            "type": "string",
                            "description": "Research topic to filter communities"
                        }
                    }
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_paper_details",
                "description": "Get detailed information about a specific paper including PDF URL",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "paper_id": {
                            "type": "string",
                            "description": "The paper ID from arXiv"
                        }
                    },
                    "required": ["paper_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "extract_paper_images",
                "description": "Download paper PDF and extract images for visual analysis",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "pdf_url": {
                            "type": "string",
                            "description": "Direct URL to PDF file"
                        }
                    },
                    "required": ["pdf_url"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_top_authors",
                "description": "Find the most prolific and influential authors",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "limit": {
                            "type": "integer",
                            "description": "Number of top authors to return"
                        }
                    }
                }
            }
        }
    ]

def execute_tool(tool_name: str, tool_input: Dict[str, Any]) -> str:
    """Execute graph and analysis tools"""
    print(f"   🛠️  Executing tool: {tool_name}")
    
    if tool_name == "pagerank_algorithm":
        limit = tool_input.get("limit", 10)
        results = graph.pagerank(limit=limit)
        return json.dumps(results)
    
    elif tool_name == "louvain_communities":
        topic = tool_input.get("topic")
        results = graph.louvain_communities(topic=topic)
        return json.dumps(results)
    
    elif tool_name == "get_paper_details":
        paper_id = tool_input.get("paper_id")
        result = graph.get_paper_details(paper_id)
        return json.dumps(result)
    
    elif tool_name == "extract_paper_images":
        pdf_url = tool_input.get("pdf_url")
        images = extract_images_from_pdf(pdf_url, max_images=3)
        return json.dumps({
            "image_count": len(images),
            "images": images[:1]  # Return first image
        })
    
    elif tool_name == "get_top_authors":
        limit = tool_input.get("limit", 10)
        results = graph.get_top_authors(limit=limit)
        return json.dumps(results)
    
    return json.dumps({"error": "Unknown tool"})

async def pipeline_3_agentic(query: str) -> dict:
    """
    Pipeline 3: Agentic Multimodal Researcher
    
    Three agent roles:
    1. INDEXER: Queries TigerGraph for papers/authors
    2. FILTER: Ranks and filters using algorithms (PageRank, Louvain)
    3. HISTORIAN: Analyzes visual content and explains findings
    """
    start_time = time.time()
    
    print(f"\n{'='*70}")
    print(f"🤖 PIPELINE 3: AGENTIC MULTIMODAL RESEARCHER")
    print(f"{'='*70}")
    print(f"Query: {query}\n")
    
    try:
        # System prompt for the agentic researcher
        system_prompt = """You are an advanced AI Research Agent with access to graph algorithms and vision analysis.

Your three roles:
1. INDEXER AGENT: Query TigerGraph using pagerank_algorithm, louvain_communities, and get_paper_details
2. FILTER AGENT: Analyze results and identify top papers/authors based on influence scores
3. HISTORIAN AGENT: When you have a paper URL, use extract_paper_images to get diagrams, then analyze them

Workflow:
- Start by understanding the query (what are we looking for?)
- Use appropriate graph algorithms to find relevant data
- Extract images from top papers when relevant
- Synthesize findings into a coherent answer

Always explain your reasoning step-by-step (chain of thought).
Use tool calls strategically - don't call all tools, only what's needed."""

        messages = [
            {
                "role": "user",
                "content": f"""You are an AI Research Agent. Answer this query using the available tools:

Query: {query}

Please:
1. Identify what information you need
2. Call the appropriate graph algorithms
3. If relevant, extract and analyze paper images
4. Provide a comprehensive answer with citations"""
            }
        ]
        
        tools = define_tools()
        
        print("⏳ Starting agentic reasoning loop...\n")
        
        # Agentic loop (up to 5 turns)
        for turn in range(5):
            print(f"Turn {turn + 1}:")
            
            # Call Mistral with tools
            response = mistral_client.chat.complete(
                model="mistral-large-latest",
                messages=messages,
                tools=tools,
                temperature=0.7
            )
            
            # Check if we're done
            if response.choices[0].finish_reason == "end_turn":
                print("   ✅ Agent finished reasoning")
                
                # Extract final answer
                final_answer = response.choices[0].message.content
                latency_ms = (time.time() - start_time) * 1000
                
                print(f"\n{'='*70}")
                print(f"✅ Final Answer Generated in {latency_ms:.0f}ms")
                print(f"{'='*70}\n")
                
                return {
                    "answer": final_answer,
                    "latency_ms": round(latency_ms, 2),
                    "tokens_in": 0,  # Mistral doesn't always expose this
                    "tokens_out": 0,
                    "tokens_total": 0,
                    "sources": ["TigerGraph", "arXiv PDFs", "Vision Analysis"],
                    "cost": 0.0,
                    "reasoning": f"Agentic Pipeline (5-turn max): Indexer → Filter → Historian",
                    "status": "success",
                    "turns": turn + 1
                }
            
            # Process tool calls
            if response.choices[0].message.tool_calls:
                print(f"   🔧 Tool calls detected: {len(response.choices[0].message.tool_calls)}")
                
                # Add assistant response to messages
                messages.append({
                    "role": "assistant",
                    "content": response.choices[0].message.content,
                    "tool_calls": response.choices[0].message.tool_calls
                })
                
                # Execute each tool
                for tool_call in response.choices[0].message.tool_calls:
                    tool_result = execute_tool(
                        tool_call.function.name,
                        tool_call.function.arguments
                    )
                    
                    # Add tool result to messages
                    messages.append({
                        "role": "tool",
                        "content": tool_result,
                        "tool_call_id": tool_call.id
                    })
                    
                    print(f"      ✅ {tool_call.function.name} executed")
            else:
                # No more tool calls, but not end_turn - break
                break
        
        # If we get here, max turns reached
        latency_ms = (time.time() - start_time) * 1000
        
        return {
            "answer": "Max reasoning turns reached. Agent provided partial answer.",
            "latency_ms": round(latency_ms, 2),
            "tokens_in": 0,
            "tokens_out": 0,
            "tokens_total": 0,
            "sources": ["TigerGraph", "arXiv PDFs"],
            "cost": 0.0,
            "reasoning": "Agentic Pipeline (max 5 turns reached)",
            "status": "partial",
            "turns": 5
        }
        
    except Exception as e:
        latency_ms = (time.time() - start_time) * 1000
        print(f"❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        
        return {
            "answer": f"❌ Error: {str(e)}",
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