from uuid import uuid4

from sqlalchemy.orm import Session

from app.database import engine
from app.services.document_service import DocumentService
from app.services.indexing_run_service import IndexingRunService
from app.services.knowledge_source_service import KnowledgeSourceService


knowledge_source_service = KnowledgeSourceService()
indexing_run_service = IndexingRunService()
document_service = DocumentService()

test_location = f"test://document-service/{uuid4()}"
knowledge_source_id = None

print("Testing document service integration...")

with Session(engine) as db:
    try:
        knowledge_source = (
            knowledge_source_service.create_knowledge_source(
                db=db,
                name="Document Service Test Source",
                source_type="test",
                location=test_location
            )
        )

        knowledge_source_id = knowledge_source.id

        indexing_run = indexing_run_service.start_indexing_run(
            db=db,
            knowledge_source_id=knowledge_source.id
        )

        document = document_service.create_document(
            db=db,
            knowledge_source_id=knowledge_source.id,
            indexing_run_id=indexing_run.id,
            filename="sample.sql",
            file_type="sql",
            file_path="database/tests/sample.sql",
            content_hash="test-content-hash",
            status="indexed"
        )

        assert document.id is not None
        assert document.knowledge_source_id == knowledge_source.id
        assert document.indexing_run_id == indexing_run.id
        assert document.filename == "sample.sql"
        assert document.status == "indexed"

        retrieved_document = (
            document_service.get_document_by_source_and_path(
                db=db,
                knowledge_source_id=knowledge_source.id,
                file_path="database/tests/sample.sql"
            )
        )

        assert retrieved_document is not None
        assert retrieved_document.id == document.id

        source_documents = (
            document_service.get_documents_by_source(
                db=db,
                knowledge_source_id=knowledge_source.id
            )
        )

        assert len(source_documents) == 1
        assert source_documents[0].id == document.id

        try:
            document_service.create_document(
                db=db,
                knowledge_source_id=knowledge_source.id,
                indexing_run_id=indexing_run.id,
                filename="sample.sql",
                file_type="sql",
                file_path="database/tests/sample.sql"
            )

            raise AssertionError(
                "Duplicate document creation should have failed."
            )

        except ValueError:
            pass

        print("Document service integration validated successfully.")
        print(f"- KnowledgeSourceRecord ID: {knowledge_source.id}")
        print(f"- IndexingRun ID: {indexing_run.id}")
        print(f"- Document ID: {document.id}")
        print("- Duplicate source-and-path registration was blocked.")

    finally:
        db.rollback()

        if knowledge_source_id is not None:
            deleted = (
                knowledge_source_service.delete_knowledge_source(
                    db=db,
                    knowledge_source_id=knowledge_source_id
                )
            )

            if deleted:
                print(
                    "Test knowledge source, indexing run, and document "
                    "were deleted."
                )