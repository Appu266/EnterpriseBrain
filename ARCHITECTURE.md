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
- LLM

---

# Current Pipeline

- File Validator
- Metadata Extractor
- Document Loader
- Reader Framework
- Chunker
- Embedding Generator
- pgvector Vector Storage

---

# Upcoming Pipeline

- Vector Similarity Search
- Retriever
- Context Builder
- LLM Response

---

# Modules

## Configuration

- config/settings.py

## Database

- app/database.py
- app/models/document.py
- app/models/document_chunk.py

## Repository

- app/repositories/document_repository.py
- app/repositories/document_chunk_repository.py

## Service

- app/services/document_service.py
- app/services/chunk_service.py

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

Last Updated: 2026-07-29
