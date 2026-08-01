# Mentor Context

---

# Project

**Name:** EnterpriseBrain

**Version:** 0.1.19

---

# Vision

## Current Goal

Build an AI assistant that understands enterprise documents, especially PL/SQL documentation and database-related assets, and can answer project-specific questions.


## Final Goal

Build a multi-language enterprise knowledge assistant capable of understanding complete software systems including Database, Java, Spring Boot, Python, .NET, React, Angular, NodeJS, APIs, Infrastructure, CI/CD and Architecture directly from repositories and enterprise documents.


---

# Current Roadmap

Current Phase : 1

### Phase 1 - Document Knowledge Assistant
Build a document-based enterprise assistant using local documents.


### Phase 2 - Database Repository Assistant
Understand complete database repositories including Oracle PL/SQL.


### Phase 3 - Backend Repository Assistant
Understand Java, Spring Boot, Python and APIs.


### Phase 4 - Frontend Repository Assistant
Understand React, Angular and NodeJS projects.


### Phase 5 - EnterpriseBrain
Unified enterprise assistant capable of understanding complete enterprise applications.




---

# Current Progress

Phase : RAG Pipeline Development

Step : Improve RAG Pipeline Quality and Prepare Enterprise Document Ingestion

Current Task :

Propagate ProcessingDocument Through the Document Ingestion Pipeline

Next Task :

Improve RAG Answer Quality and Prepare Enterprise Document Ingestion

---

# Current Architecture

## Layers

- Configuration
- Database
- ORM
- Repository
- Service
- Ingestion
- Readers
- Chunking
- Embeddings
- Vector Store
- Retrieval
- Context Builder
- QA
- LLM

## Current Pipeline

- File Validator
- Metadata Extractor
- Document Loader
- Reader Framework
- ProcessingDocument In-Memory Model
- Chunker
- Embedding Generator
- pgvector Vector Storage
- Vector Similarity Search
- Retrieval Service
- Context Builder Service
- QA Service
- Ollama LLM Integration
- RAG Answer Generation Validation

---

# Architecture Decisions

- 2026-07-28 : Repository Pattern adopted
- 2026-07-28 : Service Layer adopted
- 2026-07-28 : Knowledge schema introduced
- 2026-07-28 : Validator, Extractor and Loader separated
- 2026-07-28 : Documentation generation modularized
- 2026-07-29 : pgvector selected for vector storage
- 2026-07-29 : Sentence Transformer embeddings selected using all-MiniLM-L6-v2 model
- 2026-07-29 : Embedding vectors stored with document chunks using pgvector
- 2026-07-30 : Cosine distance selected for vector similarity search
- 2026-07-30 : Retrieval Service, Context Builder and QA Service introduced for RAG orchestration
- 2026-07-30 : LLM abstraction layer introduced to support multiple LLM providers
- 2026-07-31 : First end-to-end RAG pipeline validation completed successfully using QA flow test
- 2026-08-01 : ProcessingDocument introduced as the canonical in-memory model for documents flowing through the ingestion pipeline

---

# Assistant Instructions

- Never skip roadmap phases.
- Always continue from current_task.
- Prefer enterprise architecture.
- Prefer modular design.
- Avoid premature optimization.
- Explain every important decision.
- Keep documentation synchronized.
- Test every completed milestone.
- Provide exact terminal commands when a new file must be created.
- Provide complete replacement content for every new or modified file.
- Explain the purpose and expected outcome of each change before providing code.
- Summarize completed changes after each verified milestone.
- Do not edit project files; the user applies all changes manually.

---

# User Learning Preferences

- Teach step-by-step.
- Give whole updated file instead of suggesting manual changes.
- Explain why before how.
- Assume beginner for unfamiliar topics.
- Use enterprise best practices.
- Build incrementally.
- One task at a time.
- Avoid unnecessary complexity.
- Keep architecture consistent.

---

Last Updated : 2026-08-01
