from app.database import Base, engine

# Import every ORM model so SQLAlchemy registers all tables
# and foreign-key dependencies in Base.metadata.
from app.models.knowledge_source_record import KnowledgeSourceRecord
from app.models.indexing_run import IndexingRun
from app.models.document import Document
from app.models.document_chunk import DocumentChunk


print("Creating database tables...")

Base.metadata.create_all(bind=engine)

print("Database tables created successfully.")