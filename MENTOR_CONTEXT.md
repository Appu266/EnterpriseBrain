# Mentor Context

---

# Project

**Name:** EnterpriseBrain

**Version:** 0.1.24

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

Phase : PL/SQL Assistant MVP Development

Step : Basic Browser UI Development

Current Task :

Implement Streamlit Document Upload and Question Answering Interface

Next Task :

Validate the Complete Browser-Based Document Assistant End to End

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
- CLI
- Web UI (Upcoming)
- Presentation

## Current Pipeline

- PL/SQL Document Path Input
- Deferred AI Component Loading
- File Validator
- Metadata Extractor
- Document Loader
- Reader Framework
- ProcessingDocument In-Memory Model
- ProcessingDocument Metadata Enrichment
- ProcessingDocument Chunk Generation
- Document Database Record Creation
- Document Chunker
- Sentence Transformer Embedding Generator
- pgvector Vector Storage
- Document-Scoped Vector Similarity Search
- Retrieval Service
- Context Builder Service
- PL/SQL-Specific QA Prompt
- QA Service
- Configurable Ollama LLM Integration
- qwen2.5 1.5B Local Inference
- Interactive Question Loop
- Graceful Assistant Shutdown

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
- 2026-08-01 : DocumentLoader standardized to return ProcessingDocument with metadata and generated chunks attached
- 2026-08-01 : Interactive CLI assistant introduced as the first user-facing EnterpriseBrain interface
- 2026-08-01 : Retrieval restricted to the currently ingested document to prevent cross-document contamination of answers
- 2026-08-01 : EnterpriseBrain milestone achieved with the first complete end-to-end document ingestion and question-answering workflow
- 2026-08-01 : Complex synthetic PL/SQL package adopted for realistic MVP quality evaluation
- 2026-08-01 : PL/SQL-specific prompting introduced to improve grounded and concise answers
- 2026-08-01 : Retrieved context reduced to three chunks to balance answer quality and local inference performance
- 2026-08-01 : Ollama generation limited to 250 predicted tokens with low temperature for faster and more deterministic responses
- 2026-08-01 : Heavy AI imports deferred until after document-path input to improve perceived CLI responsiveness
- 2026-08-01 : llama3 removed because its local inference speed was impractical on the available 8 GB development laptop
- 2026-08-01 : qwen2.5:1.5b selected as the default local development LLM after reducing answer time from more than two minutes to approximately five to ten seconds
- 2026-08-01 : Ollama model name and base URL externalized through central application settings
- 2026-08-01 : Reusing stored document embeddings without source-content verification rejected to prevent stale-document answers
- 2026-08-01 : Current MVP will re-ingest the latest source file until SHA-256 based document change detection is implemented
- 2026-08-01 : Basic browser UI must be completed and validated before expanding EnterpriseBrain beyond the initial PL/SQL assistant scope
- 2026-08-01 : Assistant quality and correctness take priority over aggressive startup-time optimization
- 2026-08-02 : User Mode hides internal SQL, retrieval, embedding and ingestion diagnostics while DEBUG mode preserves them for development
- 2026-08-02 : Exact PL/SQL structural questions such as table extraction will use deterministic analysis instead of relying exclusively on the local 1.5B LLM
- 2026-08-02 : DocumentAssistantService adopted as the generic application entry point shared by CLI, Streamlit and future API-based Angular or React interfaces
- 2026-08-02 : Presentation interfaces must contain no document ingestion, retrieval, embedding or LLM orchestration logic

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
- Treat project_state.yaml as the single source of truth.
- Read committed project files directly from GitHub whenever available.
- Do not ask the user to paste files that are already committed to GitHub.
- Focus on completing the basic PL/SQL assistant end to end before expanding to additional file types.
- Complete basic UI validation before starting the next major capability iteration.
- Do not compromise answer correctness for performance improvements.
- Re-ingest the latest document content until reliable content-hash change detection is implemented.

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
- Provide PowerShell commands for creating every new file or folder.
- Return the complete updated project_state.yaml after verified milestones.
- Split project_state.yaml into contiguous parts only when required.
- Avoid repeating questions whose answers are already available.
- Prefer implementation over repeated architecture discussion.

---

Last Updated : 2026-08-02
