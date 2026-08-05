# Experimenting AI Systems 


The goal of this repository is to understand how modern AI applications are engineered in practice, including Retrieval-Augmented Generation (RAG), vector databases, embeddings, agent systems, evaluation frameworks, and scalable AI infrastructure.

---

## Repository Structure

```text
ai-sandbox/
│
├── notes/
│   ├── 01_search_in_rag.md
│   ├── 02_embeddings.md
│   ├── 03_vector_databases.md
│   ├── 04_chunking.md
│   ├── 05_bm25.md
│   └── ...
│
├── projects/
│   │
│   └── hybrid-rag-pipeline/
│       ├── app/
│       ├── data/
│       ├── requirements.txt
│       └── README.md
│
├── experiments/
│   ├── embedding_experiments.ipynb
│   ├── pinecone_test.ipynb
│   └── bm25_experiment.ipynb
│
└── README.md
```

---

## Current Learning Roadmap

### 1. Retrieval-Augmented Generation (RAG)

Topics:

* Document ingestion pipelines
* Multi-format document loaders
* Chunking strategies
* Embedding generation
* Retrieval pipelines
* Hybrid search systems

---

### 2. Search Systems

Topics:

* Dense Search
* Sparse Search
* BM25
* Semantic Search
* Hybrid Retrieval
* Reranking

---

### 3. Vector Databases

Exploring:

* Pinecone
* ChromaDB
* Qdrant

Topics:

* Similarity search
* Metadata filtering
* Approximate nearest neighbor search
* Vector indexing

---

### 4. Large Language Models

Working with:

* Local LLMs using Ollama
* API-based models
* Prompt engineering
* Context injection

---

### 5. AI Infrastructure

Learning:

* FastAPI
* Docker
* Model serving
* API architecture
* Caching systems
* Observability

---

## Current Project

## Hybrid RAG Pipeline

A production-style Retrieval-Augmented Generation system with hybrid retrieval architecture.

Planned features:

* Multi-format document ingestion
* Configurable chunking strategies
* Dense retrieval using embeddings
* Sparse retrieval using BM25
* Hybrid retrieval
* Deduplication pipeline
* Metadata-aware document indexing
* Vector database integration
* Citation tracking
* Evaluation framework

Pipeline architecture:

```text
Document Upload
        ↓
Document Loader
        ↓
Chunking Pipeline
        ↓
Embedding Generation
        ↓
Vector Database Indexing
        +
BM25 Sparse Index
        ↓
Hybrid Retrieval
        ↓
Context Assembly
        ↓
LLM Generation
        ↓
Final Answer
```

---

## Progress Log

Current progress:

* [x] AI systems learning notes started
* [ ] Multi-format document loader
* [ ] Chunking pipeline
* [ ] Embedding generation
* [ ] Vector database integration
* [ ] BM25 sparse search
* [ ] Hybrid retrieval system
* [ ] Reranking pipeline
* [ ] LLM integration
* [ ] Evaluation framework
* [ ] Deployment with Docker

##

```
```
