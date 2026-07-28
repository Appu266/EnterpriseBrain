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

---

# Upcoming Pipeline

- Reader
- Chunker
- Embedding Generator
- Vector Storage
- Retriever
- LLM Response

---

# Modules

## Configuration

- config/settings.py

## Database

- app/database.py
- app/models/document.py

## Repository

- app/repositories/document_repository.py

## Service

- app/services/document_service.py

## Ingestion

- app/validators/file_validator.py
- app/extractors/metadata_extractor.py
- app/ingestion/document_loader.py

## Readers



## Chunkers



## Embeddings



## Vector Store



---

Last Updated: 2026-07-28
