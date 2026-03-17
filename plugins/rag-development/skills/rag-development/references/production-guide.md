# Production RAG Guide

## Evaluation Metrics

| Metric | What It Measures | Range |
|--------|-----------------|-------|
| **Faithfulness** | Is the answer grounded in retrieved context? | 0-1 |
| **Answer Relevancy** | Does the answer address the query? | 0-1 |
| **Context Precision** | Are retrieved chunks relevant to the query? | 0-1 |
| **Context Recall** | Does context cover the ground truth? | 0-1 |
| **Hallucination** | Does the answer contain unsupported claims? | 0-1 |

### RAGAS
```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall

result = evaluate(
    dataset=eval_dataset,
    metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
)
print(result)
```

### DeepEval (pytest-style)
```python
from deepeval import assert_test
from deepeval.metrics import FaithfulnessMetric
from deepeval.test_case import LLMTestCase

test_case = LLMTestCase(
    input="query",
    actual_output="response",
    retrieval_context=["chunk1", "chunk2"],
)
faithfulness = FaithfulnessMetric(threshold=0.7)
assert_test(test_case, [faithfulness])
```

**Cadence**: baseline scoring weekly minimum. Trigger regression evaluations on model updates, embedding refreshes, or corpus changes.

## Observability & Tracing

| Tool | Type | Key Feature |
|------|------|-------------|
| **LangSmith** | Commercial | Deep LangChain integration, multi-step tracing |
| **Langfuse** | Open-source | Tracing, prompt versioning, dataset creation |
| **Arize Phoenix** | Open-source | Real-time observability, drift detection |

Recommended: RAGAS/DeepEval for metrics + Langfuse for observability.

## Semantic Caching

Recognizes semantically equivalent queries and returns cached answers.

**Architecture**:
1. Embed incoming query
2. Search cache index for similar past queries (cosine > 0.95 threshold)
3. Hit: return cached answer
4. Miss: execute full RAG pipeline, cache result

**Performance**:
- p95 response time: 2.1s -> 450ms
- API cost reduction: 50-80%
- Hit rate: 45-65% first week, 60-80% over time

**Advanced (RAGCache)**: Caches intermediate KV-cache states in a knowledge tree across GPU/host memory. Up to 4x TTFT reduction.

## Cost Optimization

- Matryoshka embeddings for two-stage retrieval (cheap broad, expensive narrow)
- Vector quantization (INT8 = 75% memory savings)
- Semantic caching for repeat/similar queries
- Batch embedding requests
- Smaller models for evaluation/grading tasks
- Anthropic prompt caching for contextual retrieval

## Latency Optimization

- Pre-compute embeddings at ingestion time
- Scalar quantization + in-memory for sub-ms search
- Limit retrieval to top-k 5-10 (diminishing returns beyond)
- Stream LLM responses
- Async parallel retrieval across indexes
- Matryoshka two-stage retrieval

## Security

### Prompt Injection Prevention
- Strict context adherence -- limit responses to specific tasks
- Specify clear output formats, require source citations
- Input sanitization: strip control characters, detect injection patterns
- Multi-layered defense: input filters, structured templates, output validation

### Data Access Control
- Namespace boundaries -- scope retrievers by role/purpose
- Per-user and per-query namespace restrictions via payload filtering
- Principle of least privilege for RAG application permissions
- Mandatory tenant_id filters on every query in multi-tenant systems

### PII Handling
- Filter/redact PII at ingestion before embedding
- Sanitize both user prompts and final responses
- NER (Named Entity Recognition) to detect names, emails, addresses, financial data
- Audit logging for all data access

## Frameworks & Tools

| Framework | Best For | Overhead | Connectors |
|-----------|---------|----------|-----------|
| LlamaIndex | Pure RAG, document Q&A | ~6ms | 150+ data connectors |
| LangChain | Complex agentic workflows | ~10ms | Broadest integrations |
| LangGraph | Stateful agent orchestration | ~14ms | LangChain ecosystem |
| Haystack | Production NLP, regulated | ~5.9ms | Modular pipeline components |
| DSPy | Prompt optimization | ~3.5ms | Programmatic prompt tuning |

### When to Build from Scratch
- Maximum control over latency and cost
- Highly specialized retrieval pattern
- Avoid framework lock-in
- Strong ML engineering team
- Simple pipeline (embed -> search -> generate)

A minimal RAG pipeline is ~50-100 lines of Python.

## References
- https://docs.ragas.io/
- https://docs.confident-ai.com/
- https://langfuse.com/blog/2025-10-28-rag-observability-and-evals
- https://langfuse.com/guides/cookbook/evaluation_of_rag_with_ragas
- https://deepeval.com/docs/metrics-ragas
- https://brain.co/blog/semantic-caching-accelerating-beyond-basic-rag
- https://app.ailog.fr/en/blog/guides/caching-strategies-rag
- https://genai.owasp.org/llmrisk/llm01-prompt-injection/
- https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html
- https://aws.amazon.com/blogs/security/securing-the-rag-ingestion-pipeline-filtering-mechanisms/
- https://langcopilot.com/posts/2025-09-18-top-rag-frameworks-2024-complete-guide
