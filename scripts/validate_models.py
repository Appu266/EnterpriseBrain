from sqlalchemy.orm import configure_mappers

# Import every ORM model so SQLAlchemy can configure all mappings
# and resolve relationships between them.
from app.models.knowledge_source_record import KnowledgeSourceRecord
from app.models.indexing_run import IndexingRun
from app.models.document import Document
from app.models.document_chunk import DocumentChunk


print("Validating ORM model mappings...")

configure_mappers()

print("ORM model mappings validated successfully.")
print("Validated models:")
print("- KnowledgeSourceRecord")
print("- IndexingRun")
print("- Document")
print("- DocumentChunk")