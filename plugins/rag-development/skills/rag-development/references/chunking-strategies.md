# Chunking Strategies for RAG

## Recursive Character Splitting (Default Recommendation)

Best default for most use cases. Splits hierarchically -- sections, paragraphs, sentences -- preserving structure.

**Benchmark**: Feb 2026 study of 7 strategies across 50 academic papers placed recursive 512-token splitting first at 69% accuracy; semantic chunking scored 54%.

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=64,  # ~12% overlap
    separators=["\n\n", "\n", ". ", " ", ""],
    length_function=len,
)
chunks = splitter.split_documents(documents)
```

**Parameters**:
- `chunk_size`: 400-512 tokens for general Q&A
- `chunk_overlap`: 10-20% of chunk_size
- `separators`: ordered from strongest to weakest boundary

## Markdown-Aware Chunking

Splits on headers while preserving hierarchy. Ideal for documentation, READMEs, structured technical content.

```python
from langchain.text_splitter import MarkdownHeaderTextSplitter

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]
splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
chunks = splitter.split_text(markdown_doc)
```

## Semantic Chunking

Groups content by semantic similarity rather than fixed size. Each chunk represents a coherent topic.

**Caveat**: NAACL 2025 Findings paper concluded computational costs aren't justified by consistent gains -- fixed 200-word chunks matched or beat semantic chunking across retrieval and generation tasks.

Best used when documents have highly variable topic density and compute budgets allow it.

## Parent-Child (Small-to-Big) Chunking

Index small chunks for precise retrieval, return parent chunks for LLM context.

- **Child chunks**: 128-256 tokens (embedded for retrieval)
- **Parent chunks**: 1024-2048 tokens (passed to LLM)

LlamaIndex implements this natively:
- `SentenceWindowNodeParser` -- sentence-level children with configurable window
- `HierarchicalNodeParser` -- multi-level parent-child hierarchy

## Late Chunking (Jina AI, 2024)

Embeds entire document first with long-context model, then chunks afterward. Preserves cross-chunk context (pronouns, references, headers).

**Process**:
1. Encode all tokens of entire document with full context into token-level embeddings
2. Define chunk boundaries (by sentence, paragraph, etc.)
3. Apply mean pooling within each chunk boundary

Available in `jina-embeddings-v3` API.

- Paper: https://arxiv.org/pdf/2409.04701
- Code: https://github.com/jina-ai/late-chunking

## Agentic Chunking

LLM decides chunk boundaries based on semantic coherence. Reads through the document and identifies natural topic breaks.

**Trade-off**: Expensive at indexing time but highest quality boundaries for heterogeneous documents.

## Optimal Chunk Sizes

| Use Case | Chunk Size | Overlap | Notes |
|----------|-----------|---------|-------|
| General Q&A | 400-512 tokens | 10-20% | Best default |
| Code search | 256-512 tokens | 15-25% | Preserve function boundaries |
| Legal/compliance | 512-1024 tokens | 20% | Larger context needed |
| Conversational | 128-256 tokens | 10% | Precise, focused answers |
| Summarization | 1024-2048 tokens | 10% | Broader context |

## Document Preprocessing

### Unstructured.io
Leading tool for element-level extraction. Breaks documents into typed elements (Title, NarrativeText, ListItem, Table, Image) with metadata.

- Table extraction score: 0.844
- Hallucination rate: 0.036
- Docs: https://docs.unstructured.io/open-source/introduction/overview

### Other Tools
- **LlamaParse** -- LlamaIndex integration, good for PDFs
- **Docling (IBM)** -- open-source, good accuracy
- **Apache Tika** -- broadest format support, lower accuracy

## References
- https://weaviate.io/blog/chunking-strategies-for-rag
- https://www.firecrawl.dev/blog/best-chunking-strategies-rag
- https://stackoverflow.blog/2024/12/27/breaking-up-is-hard-to-do-chunking-in-rag-applications/
- https://www.datacamp.com/tutorial/late-chunking
