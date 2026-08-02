from uuid import uuid4

from sqlalchemy.orm import Session

from app.database import engine
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.models.indexing_run import IndexingRun
from app.models.knowledge_source_record import KnowledgeSourceRecord


print("Testing database model integration...")

with Session(engine) as session:
    try:
        knowledge_source = KnowledgeSourceRecord(
            name="Database Model Test Source",
            source_type="test",
            location=f"test://database-models/{uuid4()}",
        )

        indexing_run = IndexingRun(
            status="running",
            knowledge_source=knowledge_source,
            documents_discovered=1,
        )

        document = Document(
            filename="sample.sql",
            file_type="sql",
            file_path="database/tests/sample.sql",
            status="indexed",
            knowledge_source=knowledge_source,
            indexing_run=indexing_run,
        )

        document_chunk = DocumentChunk(
            chunk_number=0,
            content="SELECT * FROM sample_table;",
            chunk_metadata={
                "start_line": 1,
                "end_line": 1,
            },
            document=document,
        )

        session.add(knowledge_source)
        session.flush()

        assert knowledge_source.id is not None
        assert indexing_run.id is not None
        assert document.id is not None
        assert document_chunk.id is not None

        assert indexing_run in knowledge_source.indexing_runs
        assert document in knowledge_source.documents
        assert document in indexing_run.documents
        assert document_chunk in document.chunks

        assert indexing_run.knowledge_source is knowledge_source
        assert document.knowledge_source is knowledge_source
        assert document.indexing_run is indexing_run
        assert document_chunk.document is document

        print("Database model integration validated successfully.")
        print("Validated records:")
        print(f"- KnowledgeSourceRecord ID: {knowledge_source.id}")
        print(f"- IndexingRun ID: {indexing_run.id}")
        print(f"- Document ID: {document.id}")
        print(f"- DocumentChunk ID: {document_chunk.id}")

    finally:
        session.rollback()
        print("Test transaction rolled back. No test data was saved.")