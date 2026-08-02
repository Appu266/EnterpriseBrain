from sqlalchemy import text

from app.database import Base, engine

# Import every ORM model so all tables are registered.
from app.models.knowledge_source_record import KnowledgeSourceRecord
from app.models.indexing_run import IndexingRun
from app.models.document import Document
from app.models.document_chunk import DocumentChunk


confirmation = input(
    "This will permanently delete the entire 'knowledge' schema and its data.\n"
    "Type RESET to continue: "
)

if confirmation != "RESET":
    print("Schema reset cancelled.")
    raise SystemExit(0)


print("Dropping and recreating the knowledge schema...")

# PostgreSQL DDL is transactional. If table creation fails,
# the entire operation is rolled back.
with engine.begin() as connection:
    connection.execute(text("DROP SCHEMA IF EXISTS knowledge CASCADE"))
    connection.execute(text("CREATE SCHEMA knowledge"))

    Base.metadata.create_all(bind=connection)


print("Knowledge schema and all tables created successfully.")