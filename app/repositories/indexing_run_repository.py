from sqlalchemy.orm import Session

from app.models.indexing_run import IndexingRun


class IndexingRunRepository:

    def create(
        self,
        db: Session,
        indexing_run: IndexingRun
    ) -> IndexingRun:

        db.add(indexing_run)
        db.commit()
        db.refresh(indexing_run)

        return indexing_run

    def get_by_id(
        self,
        db: Session,
        indexing_run_id: int
    ) -> IndexingRun | None:

        return (
            db.query(IndexingRun)
            .filter(IndexingRun.id == indexing_run_id)
            .first()
        )

    def get_all_by_source(
        self,
        db: Session,
        knowledge_source_id: int
    ) -> list[IndexingRun]:

        return (
            db.query(IndexingRun)
            .filter(
                IndexingRun.knowledge_source_id == knowledge_source_id
            )
            .order_by(IndexingRun.started_at.desc())
            .all()
        )

    def save(
        self,
        db: Session,
        indexing_run: IndexingRun
    ) -> IndexingRun:

        db.add(indexing_run)
        db.commit()
        db.refresh(indexing_run)

        return indexing_run