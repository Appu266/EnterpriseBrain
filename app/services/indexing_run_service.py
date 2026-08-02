from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.indexing_run import IndexingRun
from app.repositories.indexing_run_repository import (
    IndexingRunRepository
)


class IndexingRunService:

    def __init__(self):
        self.repository = IndexingRunRepository()

    def start_indexing_run(
        self,
        db: Session,
        knowledge_source_id: int
    ) -> IndexingRun:

        indexing_run = IndexingRun(
            knowledge_source_id=knowledge_source_id,
            status="running",
            documents_discovered=0,
            documents_processed=0,
            documents_failed=0,
            chunks_created=0
        )

        return self.repository.create(
            db,
            indexing_run
        )

    def get_indexing_run(
        self,
        db: Session,
        indexing_run_id: int
    ) -> IndexingRun | None:

        return self.repository.get_by_id(
            db,
            indexing_run_id
        )

    def get_indexing_runs_by_source(
        self,
        db: Session,
        knowledge_source_id: int
    ) -> list[IndexingRun]:

        return self.repository.get_all_by_source(
            db,
            knowledge_source_id
        )

    def complete_indexing_run(
        self,
        db: Session,
        indexing_run_id: int,
        documents_discovered: int,
        documents_processed: int,
        documents_failed: int,
        chunks_created: int
    ) -> IndexingRun:

        indexing_run = self._get_required_run(
            db,
            indexing_run_id
        )

        indexing_run.status = "completed"
        indexing_run.completed_at = datetime.now(timezone.utc)
        indexing_run.documents_discovered = documents_discovered
        indexing_run.documents_processed = documents_processed
        indexing_run.documents_failed = documents_failed
        indexing_run.chunks_created = chunks_created
        indexing_run.error_message = None

        return self.repository.save(
            db,
            indexing_run
        )

    def fail_indexing_run(
        self,
        db: Session,
        indexing_run_id: int,
        error_message: str,
        documents_discovered: int = 0,
        documents_processed: int = 0,
        documents_failed: int = 0,
        chunks_created: int = 0
    ) -> IndexingRun:

        indexing_run = self._get_required_run(
            db,
            indexing_run_id
        )

        indexing_run.status = "failed"
        indexing_run.completed_at = datetime.now(timezone.utc)
        indexing_run.documents_discovered = documents_discovered
        indexing_run.documents_processed = documents_processed
        indexing_run.documents_failed = documents_failed
        indexing_run.chunks_created = chunks_created
        indexing_run.error_message = error_message

        return self.repository.save(
            db,
            indexing_run
        )

    def _get_required_run(
        self,
        db: Session,
        indexing_run_id: int
    ) -> IndexingRun:

        indexing_run = self.repository.get_by_id(
            db,
            indexing_run_id
        )

        if indexing_run is None:
            raise ValueError(
                f"Indexing run {indexing_run_id} was not found."
            )

        return indexing_run