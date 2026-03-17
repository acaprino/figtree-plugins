# Retrieval Strategies & Patterns

## Hybrid Search (Dense + Sparse + RRF)

Combines BM25/SPLADE (keyword matching) with dense vectors (semantic matching) via Reciprocal Rank Fusion. Catches both exact tokens and semantic matches.

**RRF Formula**:
```
RRF_score(d) = sum(1 / (k + rank_i(d))) for each retrieval method i
```
Where k = 60 (standard constant).

```python
def hybrid_search(query: str, k: int = 60) -> list:
    dense_results = vector_db.search(embed(query), limit=20)
    sparse_results = bm25_index.search(query, limit=20)

    rrf_scores = {}
    for rank, doc in enumerate(dense_results):
        rrf_scores[doc.id] = rrf_scores.get(doc.id, 0) + 1 / (k + rank + 1)
    for rank, doc in enumerate(sparse_results):
        rrf_scores[doc.id] = rrf_scores.get(doc.id, 0) + 1 / (k + rank + 1)

    return sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
```

## HyDE (Hypothetical Document Embeddings)

Instead of embedding the short user query, generate a hypothetical answer with an LLM and embed that. Bridges the phrasing gap between queries and documents.

```python
def hyde_search(query: str) -> list:
    hypothetical = llm.generate(
        f"Write a detailed passage that answers: {query}"
    )
    embedding = embed(hypothetical)
    return vector_db.search(embedding, limit=10)
```

**Best for**: queries phrased very differently from how the answer appears in documents.

## Query Decomposition

Break complex multi-intent queries into sub-queries, retrieve for each, merge results.

```python
def decompose_query(query: str) -> list:
    sub_queries = llm.generate(
        f"Break this question into independent sub-questions: {query}"
    )
    all_results = []
    for sub_q in sub_queries:
        all_results.extend(retrieve(sub_q))
    return deduplicate_and_rank(all_results)
```

## Step-Back Prompting

Ask a broader, more general question first to retrieve foundational context, then use alongside the specific query.

**Example**: Query "What happens to the temperature of an ideal gas when compressed adiabatically?" -> Step-back: "What are the principles of adiabatic processes in thermodynamics?"

## Multi-Query Retrieval

Generate multiple reformulations of the original query. Captures different aspects of query intent.

```python
def multi_query_retrieve(query: str, n_variants: int = 3) -> list:
    variants = llm.generate(
        f"Generate {n_variants} different search queries for: {query}"
    )
    all_results = []
    for variant in variants:
        all_results.extend(retrieve(variant))
    return deduplicate_and_rank(all_results)
```

## Contextual Retrieval (Anthropic)

Prepend chunk-specific explanatory context before embedding and BM25 indexing. Uses LLM to generate context from the full document.

**Results**: 49% fewer failed retrievals, 67% when combined with reranking.

```python
CONTEXT_PROMPT = """
{whole_document}

Here is the chunk we want to situate within the whole document:
{chunk_content}

Give a short succinct context to situate this chunk within the overall
document for improving search retrieval. Answer only with the context.
"""

def add_context(chunk: str, document: str) -> str:
    context = llm.generate(CONTEXT_PROMPT.format(
        whole_document=document, chunk_content=chunk
    ))
    return f"{context}\n\n{chunk}"
```

**Example transformation**:
- Before: "The company's revenue grew by 3% over the previous quarter."
- After: "This chunk is from an SEC filing on ACME corp's Q2 2023 performance; previous quarter revenue was $314M. The company's revenue grew by 3% over the previous quarter."

- Blog: https://www.anthropic.com/news/contextual-retrieval
- Cookbook: https://github.com/anthropics/anthropic-cookbook/blob/main/skills/contextual-embeddings/guide.ipynb

## Re-Ranking

### Cross-Encoders
Score (query, document) pairs jointly. More accurate than bi-encoders but O(n) per query.

### Cohere Rerank
```python
import cohere
co = cohere.Client("API_KEY")
reranked = co.rerank(
    model="rerank-v3.5",
    query="query",
    documents=retrieved_docs,
    top_n=5,
)
```

### ColBERT Late Interaction
Token-level matching with MaxSim. Better than cross-encoders for longer documents.

### Two-Stage Pattern
1. Retrieve top-50 with fast vector search
2. Re-rank to top-5 with cross-encoder or Cohere Rerank
3. Pass top-5 to LLM for generation

## Self-Query / Metadata Filtering

Extract structured filters from natural language queries using an LLM.

**Example**: "Show me Python tutorials from 2024" -> query: "Python tutorials", filter: {language: "python", year: >= 2024}

## Maximal Marginal Relevance (MMR)

Balances relevance and diversity. Prevents returning near-duplicate chunks.

```
MMR = argmax[lambda * sim(q, d) - (1-lambda) * max(sim(d, d_selected))]
```
Lambda 0.5-0.7 typical. Lower = more diversity, higher = more relevance.

## Recursive / Graph-Based Retrieval

Start with initial retrieval, then follow references, links, or graph edges to retrieve related documents. Useful for multi-hop reasoning spanning multiple documents.

## References
- https://www.analyticsvidhya.com/blog/2024/12/contextual-rag-systems-with-hybrid-search-and-reranking/
- https://superlinked.com/vectorhub/articles/optimizing-rag-with-hybrid-search-reranking
- https://neo4j.com/blog/genai/advanced-rag-techniques/
- https://docs.anyscale.com/rag/quality-improvement/retrieval-strategies
