<img width="4444" height="4640" alt="system_architecture" src="https://github.com/user-attachments/assets/5c1072e9-f9b4-4cf3-ac5f-868f2f0b3be3" />

PAPERCUT: GraphRAG Research Engine
Academic research is inherently interconnected through citations, authors, and methodologies. While millions of papers are published annually, traditional retrieval systems and standard Retrieval-Augmented Generation (RAG) frameworks treat documents as isolated entities, losing the structural relationships between them.

PAPERCUT is a next-generation research engine that utilizes a Knowledge Graph-driven RAG pipeline (GraphRAG) to preserve contextual connections across academic literature.

The Limitations of Standard RAG
Standard RAG relies on vector similarity to retrieve independent text chunks based on keyword matching. This approach introduces significant limitations:

Contextual Fragmentation: It cannot naturally connect information spread across multiple documents.

Token Inefficiency: It floods the Large Language Model (LLM) with dense paragraphs of text to ensure the answer is captured, increasing operational costs and latency.

The GraphRAG Approach
PAPERCUT models a dataset of over 8,000 research papers into a unified Knowledge Graph. By structuring documents, citations, authors, and domains as interconnected nodes and edges, the retrieval pipeline explicitly traces relationship paths before querying the LLM.

Instead of reading raw text blocks, the model receives a highly distilled, structured context of exact entity relationships.

Performance Metrics
By transitioning from a flat database to an interconnected graph architecture, the system achieves significant efficiency gains over standard vector-search methods:

97% Faster Synthesis: Multi-hop queries are resolved instantly via graph traversal rather than brute-force document scanning.

75% Fewer Tokens Used: Data payloads sent to the LLM are compressed into exact facts, drastically reducing token consumption and lowering costs.

Higher Fact Precision: Mapping deterministic retrieval paths ensures the generated answers are strictly grounded in verifiable data relationships.
