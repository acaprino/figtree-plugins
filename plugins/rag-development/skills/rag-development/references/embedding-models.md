# Embedding Models & Strategies

## Commercial Models (2025-2026)

| Model | MTEB Score | Dimensions | Max Tokens | Price/MTok | Notes |
|-------|-----------|------------|------------|-----------|-------|
| Google gemini-embedding-001 | #1 overall | 768/3072 | 8192 | Free tier | Current MTEB leader |
| Cohere embed-v4 | 65.2 | 1024 | 512 | $0.10 | Best commercial API |
| OpenAI text-embedding-3-large | 64.6 | 3072 | 8191 | $0.13 | Matryoshka support |
| OpenAI text-embedding-3-small | ~62 | 1536 | 8191 | $0.02 | Best value |
| Voyage voyage-3-large | ~65 | 1024 | 32000 | $0.18 | Highest retrieval relevance |
| Mistral Embed | ~61 | 1024 | 8192 | $0.01 | Cheapest commercial |

## Open-Source Models

| Model | MTEB Score | Dimensions | Notes |
|-------|-----------|------------|-------|
| NV-Embed-v2 | 72.3 | 4096 | Beats all commercial on English MTEB |
| BGE-M3 | 63.0 | 1024 | Excellent multilingual |
| Jina-embeddings-v3 | ~63 | 1024 | Late chunking support, 8192 context |
| Nomic-embed-text-v1.5 | ~62 | 768 | Good Matryoshka support |

## Embedding Types

### Dense Vectors (Semantic Meaning)
Single fixed-size vector per chunk. Models like OpenAI, Cohere, Voyage produce vectors capturing semantic meaning. Standard approach.

### Sparse Vectors (Keyword/Lexical)
High-dimensional vectors where each dimension = vocabulary term. BM25 or neural sparse models (SPLADE). Best for exact keyword matching, domain terminology, IDs, acronyms.

### Multi-Vector / ColBERT (Late Interaction)
One vector per token. At search time, MaxSim operator finds passages with contextually matching tokens. More nuanced than single-vector but requires more storage.

```python
from ragatouille import RAGPretrainedModel

RAG = RAGPretrainedModel.from_pretrained("colbert-ir/colbertv2.0")
RAG.index(
    collection=documents,
    index_name="my_index",
    max_document_length=256,
    split_documents=True,
)
results = RAG.search(query="search query", k=5)
```

## Matryoshka Embeddings

Trained so first N dimensions form a valid (lower-quality) embedding. Enables:
- **Adaptive retrieval**: 256-dim for fast candidate selection, full-dim for re-ranking
- **Storage optimization**: store smaller embeddings, expand when needed

Supported by: OpenAI text-embedding-3-*, Nomic-embed-text-v1.5, Jina-ColBERT-v2

**Two-stage pattern**:
```python
# Stage 1: Fast candidate retrieval with small embeddings
candidates = vector_db.search(query_embedding[:256], limit=100)

# Stage 2: Re-rank with full embeddings
reranked = rerank_by_full_similarity(query_embedding, candidates)
```

## Fine-Tuning Embeddings

Domain-specific fine-tuning improves retrieval by 5-15% on specialized corpora.

**Approaches**:
- Contrastive learning on (query, positive_doc, negative_doc) triplets
- Synthetic data: use LLM to generate questions from your documents
- `sentence-transformers` library for training
- Cohere and Voyage offer fine-tuning APIs

## Embedding Caching

- Cache embeddings at ingestion time (never re-embed unchanged documents)
- Content hashing to detect document changes
- Store embeddings alongside metadata in vector DB
- Query embedding cache with TTL for frequent queries

## Selection Guide

- budget-conscious, general use -> OpenAI text-embedding-3-small
- highest accuracy, commercial -> Voyage voyage-3-large or Cohere embed-v4
- self-hosted, no API dependency -> NV-Embed-v2 or BGE-M3
- multilingual -> BGE-M3 or Cohere embed-multilingual-v3
- late chunking needed -> Jina-embeddings-v3
- maximum storage efficiency -> Matryoshka with dimension truncation

## References
- MTEB Leaderboard: https://huggingface.co/spaces/mteb/leaderboard
- https://app.ailog.fr/en/blog/guides/choosing-embedding-models
- https://reintech.io/blog/embedding-models-comparison-2026-openai-cohere-voyage-bge
- https://weaviate.io/developers/weaviate/tutorials/multi-vector-embeddings
- https://weaviate.io/blog/late-interaction-overview
- https://qdrant.tech/documentation/fastembed/fastembed-colbert/
- https://til.simonwillison.net/llms/colbert-ragatouille
