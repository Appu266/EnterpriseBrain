# EnterpriseBrain Architecture

---

# Architecture Style

- Layered Architecture
- Repository Pattern
- Service Pattern
- Configuration-Driven LLM Integration
- Factory Pattern (Upcoming)
- Strategy Pattern (Upcoming)
- Knowledge Source Abstraction
- Factory Pattern

---

# Layers

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
- Streamlit Browser UI
- Repository Discovery
- Repository Reading
- Repository Ingestion
- Knowledge Source Management

---

# Current Pipeline

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
- Browser Document Upload
- Streamlit Session State
- Generic DocumentAssistantService
- Conversation-Aware Retrieval Query
- Conversation History Prompt Context
- Browser Chat Interface

---

# Upcoming Pipeline

- Git Repository Source
- Repository Cloning or Local Repository Selection
- Recursive Repository File Discovery
- Database Source File Filtering
- Repository and File Metadata Extraction
- Multi-File Repository Ingestion
- Repository-Scoped Vector Retrieval
- Cross-File Database Question Answering
- Database Object Dependency Foundation
- Retrieval Quality Improvement
- Prompt Quality Improvement
- Source Attribution Improvement
- Hash-Based Document Change Detection
- Persistent Application Runtime
- Enterprise Document Ingestion
- Metadata Enhancement
- Document Classification
- SHA-256 Document Content Hashing
- Duplicate Document Detection
- Existing Embedding Reuse
- PDF Reader
- DOCX Reader
- FastAPI Application Interface
- Angular or React Enterprise UI

---

# Modules

## Configuration

- config/settings.py

## Database

- app/database.py
- app/models/document.py
- app/models/document_chunk.py
- app/models/processing_document.py

## Repository

- app/repositories/document_repository.py
- app/repositories/document_chunk_repository.py

## Service

- app/services/document_service.py
- app/services/chunk_service.py
- app/services/retrieval_service.py
- app/services/context_builder_service.py
- app/services/qa_service.py
- app/services/document_assistant_service.py

## Ingestion

- app/validators/file_validator.py
- app/extractors/metadata_extractor.py
- app/ingestion/document_loader.py

## Readers

- app/readers/base_reader.py
- app/readers/txt_reader.py

## Chunkers

- app/chunkers/document_chunker.py
- app/chunkers/text_chunker.py

## Embeddings

- app/embeddings/embedding_generator.py

## Vector Store

- pgvector

---

Last Updated: 2026-08-02
