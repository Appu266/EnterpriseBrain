# EnterpriseBrain Architecture

---

# Architecture Style

- Layered Architecture
- Repository Pattern
- Service Pattern
- Factory Pattern (Upcoming)
- Strategy Pattern (Upcoming)

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

---

# Current Pipeline

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

# Upcoming Pipeline

- ProcessingDocument Pipeline Propagation
- Prompt Engineering Layer
- Enterprise Document Ingestion
- Metadata Enhancement
- Document Classification

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

Last Updated: 2026-08-01
