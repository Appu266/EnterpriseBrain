# EnterpriseBrain - Architecture

## Project Vision

EnterpriseBrain is an AI-powered Enterprise Knowledge Assistant that enables users to search, retrieve, and understand enterprise documents using Retrieval-Augmented Generation (RAG), vector search, and Large Language Models (LLMs).

---

# Technology Stack

| Layer | Technology | Status |
|--------|------------|--------|
| Programming Language | Python 3.12 | Finalized |
| Database | PostgreSQL 18 | Finalized |
| Database Administration | pgAdmin | Finalized |
| Container Platform | Docker Desktop | Finalized |
| IDE | PyCharm | Finalized |
| Vector Extension | pgvector | Planned |
| API Framework | FastAPI | Planned |
| ORM | SQLAlchemy | Planned |
| AI Framework | LangChain | Planned |
| Embedding Model | TBD | Pending |
| LLM | TBD | Pending |

---

# High-Level Architecture

User

↓

FastAPI

↓

Business Logic

↓

Vector Search

↓

PostgreSQL + pgvector

↓

Enterprise Documents

---

# Directory Structure

app/
Business logic

config/
Application configuration

data/
Input documents

docker/
Container configuration

docs/
Documentation

logs/
Application logs

scripts/
Utility scripts

storage/
Generated application data

tests/
Automated testing

---

# Architecture Principles

- Clean and modular architecture
- Separation of concerns
- Configuration outside code
- Scalable project structure
- Production-ready design
- Docker-first deployment
- PostgreSQL as the single database

---

# Future Components

- Authentication
- Authorization
- Document ingestion pipeline
- Chunking engine
- Embedding service
- Semantic search
- Prompt management
- Conversation history
- Monitoring
- Logging
- REST APIs
- Admin dashboard

---

# Architecture Decision Log

| Date | Decision |
|------|----------|
| 28-Jul-2026 | PostgreSQL selected as primary database |
| 28-Jul-2026 | Docker selected for containerization |
| 28-Jul-2026 | PyCharm selected as IDE |
| 28-Jul-2026 | Enterprise project structure finalized |

---

Last Updated:
28-Jul-2026