# Retrieval-Augmented Generation (RAG)

## Overview

Retrieval-Augmented Generation (RAG) is an architectural pattern that combines external knowledge retrieval with language model generation to produce accurate, grounded responses. Instead of relying solely on a model's parametric knowledge (what it learned during training), RAG dynamically fetches relevant information from a knowledge base at inference time.

---

## Core Concept

RAG separates the **knowledge storage** from the **reasoning engine**. This modular architecture allows:

- **Knowledge updates without retraining** — Update the knowledge base independently of the model
- **Reduced hallucination** — Ground responses in verified, retrieved sources
- **Cost efficiency** — Avoid expensive fine-tuning for domain-specific applications
- **Transparency** — Cite sources and show where information came from

---

## How RAG Works

### The Pipeline

```
User Query → Embedding → Vector Search → Retrieved Documents → Prompt Assembly → LLM Generation → Response
```

### Step-by-Step Breakdown

1. **Indexing Phase** (One-time setup)
   - Documents are chunked into manageable segments
   - Each chunk is converted to a vector embedding using an embedding model
   - Embeddings are stored in a vector database for fast similarity search

2. **Retrieval Phase** (At query time)
   - User query is converted to an embedding using the same model
   - Semantic search finds the most relevant document chunks
   - Top-k results are retrieved based on similarity scores

3. **Augmentation Phase**
   - Retrieved context is formatted into a prompt template
   - System instruction tells the LLM to use only the provided context
   - Query + Context + Instructions are combined into a single prompt

4. **Generation Phase**
   - LLM generates a response grounded in the retrieved context
   - Citations or source references can be included in the output

---

## Key Components

### 1. Document Chunking
- **Fixed-size chunking**: Split by token/character count (e.g., 500 tokens)
- **Semantic chunking**: Split by meaning boundaries (paragraphs, sections)
- **Recursive chunking**: Hierarchical splitting with overlap
- **Overlap**: 10-20% overlap between chunks to preserve context

### 2. Embedding Models
- **OpenAI**: text-embedding-ada-002, text-embedding-3-small, text-embedding-3-large
- **Open Source**: BGE, E5, Sentence Transformers, Jina Embeddings
- **Properties**: 384-3072 dimensions, optimized for different tasks

### 3. Vector Databases
- **Purpose-built**: Pinecone, Weaviate, Milvus, Qdrant, Chroma
- **Traditional with vector support**: PostgreSQL (pgvector), MongoDB, Redis
- **Key features**: Approximate Nearest Neighbor (ANN), metadata filtering, hybrid search

### 4. Retrieval Strategies
- **Dense retrieval**: Pure vector similarity (semantic search)
- **Sparse retrieval**: Keyword matching (BM25, TF-IDF)
- **Hybrid retrieval**: Combine dense + sparse for best results
- **Re-ranking**: Cross-encoder re-ranking of top candidates for improved precision

### 5. Prompt Construction
- Context window management (fit within model limits)
- Relevance filtering (remove irrelevant retrieved chunks)
- Source attribution (include citations/references)

---

## Advanced RAG Techniques

### 1. Query Transformations
- **Query expansion**: Generate multiple query variants
- **Step-back prompting**: Generate a broader query to retrieve general context
- **Sub-query decomposition**: Break complex queries into simpler sub-queries
- **HyDE (Hypothetical Document Embeddings)**: Generate a hypothetical answer, then embed it for search

### 2. Context Enrichment
- **Sentence window retrieval**: Retrieve surrounding sentences for context
- **Auto-merging retrieval**: Combine small chunks into coherent context blocks
- **Parent document retrieval**: Retrieve child chunks, return parent documents

### 3. Re-ranking
- **Cross-encoder re-ranking**: More accurate scoring of top candidates
- **LLM-based re-ranking**: Use an LLM to score relevance
- **Metadata-aware re-ranking**: Incorporate freshness, authority, source type

### 4. Multi-Modal RAG
- Image retrieval with CLIP embeddings
- Audio/video transcription and embedding
- Table/chart extraction and understanding

---

## Code Example

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

# 1. Load and chunk documents
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " ", ""]
)
chunks = text_splitter.split_documents(documents)

# 2. Create embeddings and store in vector database
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma.from_documents(chunks, embeddings)

# 3. Create retriever
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4}  # Return top 4 most relevant chunks
)

# 4. Set up LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 5. Create RAG chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True
)

# 6. Query
result = qa_chain.invoke("What are the benefits of RAG over fine-tuning?")
print(result["result"])
print("\nSources:", result["source_documents"])
```

---

## Benefits vs. Limitations

### Benefits
| Benefit | Description |
|---------|-------------|
| **Reduced Hallucination** | 60-80% reduction by grounding in verified sources |
| **Cost Efficient** | No need for expensive fine-tuning runs |
| **Up-to-Date Knowledge** | Update knowledge base without retraining |
| **Source Attribution** | Cite sources, show provenance |
| **Domain-Specific** | Easy to customize for any domain |
| **Modular** | Swap components independently |

### Limitations
| Limitation | Mitigation |
|------------|------------|
| **Retrieval quality** | Better chunking, re-ranking, hybrid search |
| **Context window limits** | Intelligent context selection, compression |
| **Latency** | Caching, pre-computation, optimized retrieval |
| **Knowledge base maintenance** | Automated update pipelines |
| **Multi-hop reasoning** | Iterative retrieval, agentic approaches |

---

## RAG vs. Fine-Tuning

| Aspect | RAG | Fine-Tuning |
|--------|-----|-------------|
| **Knowledge** | External, dynamic | Internal, static |
| **Updates** | Instant (update KB) | Expensive (retrain) |
| **Hallucination** | Lower (grounded) | Higher (parametric) |
| **Cost** | Lower (API calls only) | Higher (training compute) |
| **Transparency** | High (citable sources) | Low (black box) |
| **Best For** | Factual, domain-specific | Style, format, behavior |

> **Key Insight**: RAG is the primary pattern for domain-specific AI applications. Fine-tuning is better suited for changing model behavior or format rather than injecting knowledge.

---

## Industry Adoption

- Enterprises are adopting RAG as the **primary pattern** for domain-specific AI applications
- Organizations implementing RAG report **60-80% reduction in hallucination rates**
- Vector database market grew **10x in two years** as RAG adoption accelerated
- RAG will evolve toward **multi-modal retrieval** and **real-time knowledge updating**

---

## Popular Frameworks & Tools

| Tool | Purpose |
|------|---------|
| **LangChain** | Orchestration, chains, agents |
| **LlamaIndex** | Data connectors, indexing, retrieval |
| **Haystack** | End-to-end RAG pipelines |
| **Chroma** | Lightweight vector database |
| **Pinecone** | Managed vector database |
| **Weaviate** | Open-source vector database |
| **Cohere Rerank** | Re-ranking service |

---

## Future Directions

1. **Multi-Modal RAG**: Retrieving across text, images, audio, video
2. **Agentic RAG**: Autonomous iterative retrieval and verification
3. **Real-Time Knowledge**: Live data feeds and streaming updates
4. **Personalized RAG**: User-specific context and preferences
5. **Self-Correcting RAG**: Automatic fact-checking and correction
6. **Federated RAG**: Distributed knowledge bases across organizations

---

## Key Resources

- **Paper**: "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" (Lewis et al., 2020)
- **LangChain RAG Docs**: https://python.langchain.com/docs/tutorials/rag/
- **LlamaIndex Guides**: https://docs.llamaindex.ai/en/stable/
- **Pinecone RAG Overview**: https://www.pinecone.io/learn/series/langchain/rag/

---

*Last Updated: April 5, 2026*
