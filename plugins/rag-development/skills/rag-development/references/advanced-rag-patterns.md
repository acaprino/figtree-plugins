# Advanced RAG Patterns

## Agentic RAG

Agent orchestrates retrieval dynamically -- decides when to retrieve, which indexes to query, whether to refine the query, and when to stop.

**Architecture**:
```
User Query -> Agent (LLM)
  -> Decide: retrieve? which index? transform query?
  -> Execute retrieval
  -> Evaluate: sufficient? accurate?
  -> If not: re-query, use different tool, decompose
  -> Generate final answer
```

Frameworks: LangGraph agents, LlamaIndex `AgentRunner`, CrewAI with RAG tools.

- Survey: https://github.com/asinghcsu/AgenticRAG-Survey

## Graph RAG (Microsoft)

Builds a knowledge graph from documents, detects community structures, generates hierarchical summaries, then uses these for retrieval.

**Process**:
1. LLM extracts entities (nodes) and relationships (edges) from text chunks
2. Community detection partitions the graph hierarchically (Leiden algorithm)
3. LLM generates summaries for each community at each level
4. At query time, searches both graph structure and community summaries

**Best for**: themes, narratives, cross-document reasoning, "what are the main themes across these documents?"

- Code: https://github.com/microsoft/graphrag
- Docs: https://microsoft.github.io/graphrag/
- Paper: https://arxiv.org/html/2404.16130v1

## RAPTOR (Recursive Abstractive Processing for Tree-Organized Retrieval)

Hierarchical tree of summaries from leaf chunks up to root summaries.

**Process**:
1. Embed and cluster leaf chunks by semantic similarity
2. Summarize each cluster
3. Embed summaries, cluster again, summarize again
4. Repeat until single root summary
5. At query time, traverse tree from root to leaves

**Best for**: long-context Q&A where answers span multiple parts of a document.

- Code: https://github.com/parthsarthi03/raptor

## Corrective RAG (CRAG)

Adds a retrieval evaluator that grades retrieved documents before passing to LLM.

**Flow**:
1. Retrieve documents
2. Evaluator grades each: "Correct", "Ambiguous", or "Incorrect"
3. Correct -> use for generation
4. Ambiguous -> refine query, re-retrieve
5. Incorrect -> fall back to web search or alternative sources

## Self-RAG

Model decides when to retrieve and self-critiques outputs for factuality.

**Special tokens**:
- `[Retrieve]` -- should I retrieve? (yes/no)
- `[IsRel]` -- is retrieved passage relevant?
- `[IsSup]` -- is response supported by passage?
- `[IsUse]` -- is response useful?

## Modular RAG

RAG as interchangeable modules:
- **Router** -- directs queries to appropriate retrieval pipeline
- **Retriever** -- multiple types (dense, sparse, graph)
- **Evaluator** -- scores retrieved context quality
- **Generator** -- LLM for answer synthesis
- **Refiner** -- post-processes and validates outputs

## Multi-Modal RAG

### Tables
- Extract as HTML (preserves structure best)
- Embed with text models or summarize with LLM
- Store both raw table and LLM summary

### Images
- Multimodal embeddings (CLIP, SigLIP) for image-text matching
- Vision LLMs to generate text descriptions for indexing
- ColPali/ColQwen: late-interaction models for document page images (no OCR needed)

### PDFs
- Unstructured.io for element-level extraction
- LlamaParse for LlamaIndex integration
- Consider page-level indexing with vision models for complex layouts

## Pattern Selection Guide

| Pattern | Complexity | Best For | When to Use |
|---------|-----------|---------|------------|
| Naive RAG | Low | Simple Q&A, clean docs | Start here |
| Hybrid + Reranking | Medium | Most production use cases | Keyword misses or irrelevant results |
| Contextual Retrieval | Medium | Ambiguous chunks | 49-67% fewer retrieval failures |
| Agentic RAG | High | Complex multi-hop queries | Simple retrieval insufficient |
| Graph RAG | High | Cross-document themes | Need to reason across many documents |
| RAPTOR | High | Long documents | Answers span multiple doc sections |
| CRAG | Medium | Unreliable corpus | Retrieved docs often irrelevant |
| Self-RAG | High | Variable query types | Some queries don't need retrieval |

## References
- https://dev.to/naresh_007/beyond-vanilla-rag-the-7-modern-rag-architectures-every-ai-engineer-must-know-4l0c
- https://datanucleus.dev/rag-and-agentic-ai/what-is-rag-enterprise-guide-2025
- https://contextual.ai/blog/an-agentic-alternative-to-graphrag
