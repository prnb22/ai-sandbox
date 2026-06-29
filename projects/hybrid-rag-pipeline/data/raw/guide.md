# Hybrid RAG Implementation Guide v2.1

## Overview
This document outlines the evaluation metrics for our vector and keyword search layers.

## Hybrid Search Fusion Configuration
We use Reciprocal Rank Fusion (RRF) to merge query results.

| Parameter | Default Value | Description |
| :--- | :--- | :--- |
| `alpha` | 0.5 | Weight for Dense vs Sparse (1.0 is pure vector) |
| `top_k` | 10 | Total documents returned to the LLM |

