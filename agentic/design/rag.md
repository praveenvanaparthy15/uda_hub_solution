# UDA-Hub — RAG Design

## Purpose

UDA-Hub uses Retrieval-Augmented Generation to ground customer support responses in the CultPass knowledge base.

## Pipeline

```text
Knowledge Articles
       |
       v
Document Preparation
       |
       v
Embeddings
       |
       v
FAISS Vector Store
       |
       v
Semantic Similarity Search
       |
       v
Top Relevant Articles
       |
       v
Confidence Evaluation
       |
       +------ Relevant ------> Resolver
       |
       +------ Not Relevant -> Escalation
```

## Knowledge Source

The primary knowledge source is the `Knowledge` table in the UDA-Hub SQLite database.

The knowledge base contains support information covering:

* Account
* Technical issues
* Billing
* Subscription
* Booking
* Refunds
* Promotional codes
* Escalation

## Retrieval

The customer's ticket description is converted into an embedding.

The embedding is compared against knowledge article embeddings using semantic similarity.

The most relevant articles are returned to the Resolver.

## Grounding

The Resolver should use retrieved articles as the source for customer-facing answers.

The system should not invent policies, refund amounts, subscription rules, or other unsupported information.

## Confidence

A configurable similarity threshold is used.

High similarity:

```text
Retrieve article
       |
       v
Resolver
```

Low similarity:

```text
No reliable article
       |
       v
Escalation Agent
```

## Benefits

RAG allows UDA-Hub to:

* Handle natural-language customer questions.
* Retrieve relevant support information.
* Reduce unsupported answers.
* Support multiple knowledge categories.
* Provide a clear escalation path when knowledge is insufficient.
