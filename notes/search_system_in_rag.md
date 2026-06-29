# Understanding Search in RAG Systems

In Retrieval-Augmented Generation (RAG) systems, retrieval is one of the most important components. Before sending context to the Large Language Model (LLM), the system must retrieve relevant information from stored documents.

Modern RAG systems mainly use three search approaches:

* Sparse Search
* Dense Search
* Hybrid Search

---

# 1. Sparse Search (Keyword-Based Retrieval)

Sparse search is the traditional retrieval approach based on **exact keyword matching**.

It does **not understand meaning**. It only checks whether specific words exist inside documents.

Example query:

```text
What does REDIS_PORT do?
```

Documents:

```text
Document A:
Set REDIS_PORT=6379 in redis.conf

Document B:
Redis uses configuration variables for network communication
```

Sparse search prefers **Document A** because it contains the exact keyword **REDIS_PORT**.

---

## BM25 Algorithm

The most common sparse retrieval algorithm is **BM25 (Best Matching 25)**.

BM25 ranks documents using three important factors.

---

### A. Term Frequency (TF)

Term Frequency measures how many times a query word appears inside a document.

Example:

```text
REDIS_PORT REDIS_PORT REDIS_PORT
```

More occurrences → higher score.

---

### B. Inverse Document Frequency (IDF)

IDF measures how rare a word is across all documents.

Common word:

```text
the
```

Appears everywhere → low importance.

Rare word:

```text
REDIS_PORT
```

Appears rarely → high importance.

Rare words receive higher scores.

---

### C. Document Length Normalization

Long documents should not automatically rank higher.

Example:

```text
Document A = 50 words

Document B = 5000 words
```

If both contain the keyword, BM25 adjusts scores so long documents do not unfairly dominate.

---

## BM25 Scoring Intuition

A document gets higher score when:

* Query word appears many times
* Query word is rare in the document collection
* Document is shorter and more focused

Simplified idea:

```text
Higher Score = More keyword frequency + Rarer keyword + Shorter relevant document
```

---

## BM25 Example

Query:

```text
REDIS_PORT
```

Documents:

```text
Doc 1:
Redis configuration guide

Doc 2:
Set REDIS_PORT=6379 in redis.conf

Doc 3:
Docker network tutorial
```

Possible scores:

```text
Doc 1 → 0.2

Doc 2 → 2.8

Doc 3 → 0.1
```

Document 2 gets highest score because it contains the exact keyword.

---

## Python Example

```python
from rank_bm25 import BM25Okapi

documents = [
    "Redis configuration guide",
    "Set REDIS_PORT=6379 in redis.conf",
    "Docker network tutorial"
]

tokenized_docs = [doc.split() for doc in documents]

bm25 = BM25Okapi(tokenized_docs)

query = "REDIS_PORT".split()

scores = bm25.get_scores(query)
```

---

# 2. Dense Search (Semantic Retrieval)

Dense search uses **embeddings** instead of exact keyword matching.

An embedding model converts text into numerical vectors.

Example:

```text
I want to learn Python programming
```

↓

```text
[0.12, 0.76, 0.44, ...]
```

Similar meaning → vectors become close together.

---

## What is Semantic Meaning?

Semantic meaning means understanding the **intent behind text instead of exact words**.

Example:

Sentence 1:

```text
I want to learn Python programming
```

Sentence 2:

```text
I want to study Python development
```

Different words:

```text
learn ≠ study

programming ≠ development
```

But both sentences have similar meaning.

Dense retrieval understands this similarity.

---

## Dense Search Example

User asks:

```text
How do I deploy Docker applications?
```

Document:

```text
Docker is used to run containerized software.
```

Different words:

```text
deploy ≠ run

applications ≠ software
```

Dense search understands both have similar meaning.

---

## How Dense Search Works

```text
Text
 ↓
Embedding Model
 ↓
Vector Representation
 ↓
Store in Vector Database
 ↓
Similarity Search
 ↓
Return nearest vectors
```

Popular vector databases:

* ChromaDB
* Qdrant
* Pinecone
* Weaviate

---

## Similarity Search

Suppose query vector:

```text
[0.2, 0.5, 0.9]
```

Stored vectors:

```text
Doc A → [0.21, 0.49, 0.88]

Doc B → [0.80, 0.10, 0.20]
```

Distance calculation methods:

* Cosine Similarity
* Euclidean Distance

Nearest vectors are retrieved.

---

# 3. Hybrid Search

Hybrid search combines:

```text
Dense Search + Sparse Search
```

because each method solves different problems.

---

## Problem with Dense Search

Dense retrieval understands meaning but may miss exact technical keywords.

Example:

```text
Question:
What does REDIS_PORT do?
```

Dense retrieval may return:

```text
Redis configuration documentation
```

but miss:

```text
REDIS_PORT=6379
```

---

## Problem with Sparse Search

Sparse search finds exact keywords but cannot understand meaning.

Example:

Query:

```text
How do I run Docker containers?
```

Document:

```text
Deploying applications with Docker Compose
```

Sparse retrieval may fail because words are different.

---

# Hybrid Search Architecture

```text
User Question
        ↓
Dense Retrieval (Embeddings)
        +
Sparse Retrieval (BM25)
        ↓
Combine results
        ↓
Return best matching documents
        ↓
Send context to LLM
```

---

# Comparison Table

| Search Type   | Works On         | Strength                    | Weakness                  |
| ------------- | ---------------- | --------------------------- | ------------------------- |
| Sparse Search | Exact words      | Good for technical keywords | Cannot understand meaning |
| Dense Search  | Semantic meaning | Understands intent          | May miss exact keywords   |
| Hybrid Search | Both             | Highest retrieval quality   | More system complexity    |

---

# Which Systems Use Which Search?

Traditional search engines:

```text
Sparse Search
```

Modern AI systems:

```text
Dense Search
```

Production RAG systems:

```text
Hybrid Search
```

---

# Key Understanding

```text
Sparse Search = Looks at exact words

Dense Search = Looks at meaning

Hybrid Search = Combines both
```

---

# Important Engineering Understanding

Dense retrieval improves semantic understanding.

Sparse retrieval improves exact keyword precision.

Hybrid retrieval improves overall retrieval quality.

Because retrieval quality directly affects the final LLM answer, production-grade RAG systems often combine both approaches.

---

# Final Mental Model

```text
Sparse Search → Exact keyword matching

Dense Search → Semantic understanding

Hybrid Search → Production-level retrieval
```
