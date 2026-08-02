from sqlalchemy.orm import Session

from app.models.knowledge_source_record import KnowledgeSourceRecord


class KnowledgeSourceRepository:

    def create(
        self,
        db: Session,
        knowledge_source: KnowledgeSourceRecord
    ) -> KnowledgeSourceRecord:

        db.add(knowledge_source)
        db.commit()
        db.refresh(knowledge_source)

        return knowledge_source

    def get_by_id(
        self,
        db: Session,
        knowledge_source_id: int
    ) -> KnowledgeSourceRecord | None:

        return (
            db.query(KnowledgeSourceRecord)
            .filter(
                KnowledgeSourceRecord.id == knowledge_source_id
            )
            .first()
        )

    def get_by_type_and_location(
        self,
        db: Session,
        source_type: str,
        location: str
    ) -> KnowledgeSourceRecord | None:

        return (
            db.query(KnowledgeSourceRecord)
            .filter(
                KnowledgeSourceRecord.source_type == source_type,
                KnowledgeSourceRecord.location == location
            )
            .first()
        )

    def get_all(
        self,
        db: Session
    ) -> list[KnowledgeSourceRecord]:

        return (
            db.query(KnowledgeSourceRecord)
            .order_by(KnowledgeSourceRecord.id)
            .all()
        )

    def delete(
        self,
        db: Session,
        knowledge_source: KnowledgeSourceRecord
    ) -> None:

        db.delete(knowledge_source)
        db.commit()