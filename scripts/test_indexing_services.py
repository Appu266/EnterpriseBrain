from uuid import uuid4

from sqlalchemy.orm import Session

from app.database import engine
from app.services.indexing_run_service import IndexingRunService
from app.services.knowledge_source_service import KnowledgeSourceService


knowledge_source_service = KnowledgeSourceService()
indexing_run_service = IndexingRunService()

test_location = f"test://indexing-services/{uuid4()}"
knowledge_source_id = None

print("Testing knowledge-source and indexing-run services...")

with Session(engine) as db:
    try:
        knowledge_source = (
            knowledge_source_service.create_knowledge_source(
                db=db,
                name="Indexing Service Test Source",
                source_type="test",
                location=test_location
            )
        )

        knowledge_source_id = knowledge_source.id

        assert knowledge_source.id is not None
        assert knowledge_source.indexing_status == "registered"
        assert knowledge_source.is_active is True

        retrieved_source = (
            knowledge_source_service
            .get_knowledge_source_by_type_and_location(
                db=db,
                source_type="test",
                location=test_location
            )
        )

        assert retrieved_source is not None
        assert retrieved_source.id == knowledge_source.id

        indexing_run = indexing_run_service.start_indexing_run(
            db=db,
            knowledge_source_id=knowledge_source.id
        )

        assert indexing_run.id is not None
        assert indexing_run.status == "running"
        assert indexing_run.documents_discovered == 0

        completed_run = indexing_run_service.complete_indexing_run(
            db=db,
            indexing_run_id=indexing_run.id,
            documents_discovered=3,
            documents_processed=2,
            documents_failed=1,
            chunks_created=8
        )

        assert completed_run.status == "completed"
        assert completed_run.completed_at is not None
        assert completed_run.documents_discovered == 3
        assert completed_run.documents_processed == 2
        assert completed_run.documents_failed == 1
        assert completed_run.chunks_created == 8
        assert completed_run.error_message is None

        run_history = (
            indexing_run_service.get_indexing_runs_by_source(
                db=db,
                knowledge_source_id=knowledge_source.id
            )
        )

        assert len(run_history) == 1
        assert run_history[0].id == completed_run.id

        print("Service-layer integration validated successfully.")
        print(f"- KnowledgeSourceRecord ID: {knowledge_source.id}")
        print(f"- IndexingRun ID: {completed_run.id}")
        print("- Indexing run completed with the expected counters.")

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
                    "Test knowledge source and its indexing run "
                    "were deleted."
                )