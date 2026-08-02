from sqlalchemy.orm import Session

from app.models.knowledge_source_record import KnowledgeSourceRecord
from app.repositories.knowledge_source_repository import (
    KnowledgeSourceRepository
)


class KnowledgeSourceService:

    def __init__(self):
        self.repository = KnowledgeSourceRepository()

    def create_knowledge_source(
        self,
        db: Session,
        name: str,
        source_type: str,
        location: str
    ) -> KnowledgeSourceRecord:

        existing_source = self.repository.get_by_type_and_location(
            db,
            source_type,
            location
        )

        if existing_source is not None:
            raise ValueError(
                "A knowledge source with this type and location "
                "is already registered."
            )

        knowledge_source = KnowledgeSourceRecord(
            name=name,
            source_type=source_type,
            location=location,
            indexing_status="registered",
            is_active=True
        )

        return self.repository.create(
            db,
            knowledge_source
        )

    def get_knowledge_source(
        self,
        db: Session,
        knowledge_source_id: int
    ) -> KnowledgeSourceRecord | None:

        return self.repository.get_by_id(
            db,
            knowledge_source_id
        )

    def get_knowledge_source_by_type_and_location(
        self,
        db: Session,
        source_type: str,
        location: str
    ) -> KnowledgeSourceRecord | None:

        return self.repository.get_by_type_and_location(
            db,
            source_type,
            location
        )

    def get_knowledge_sources(
        self,
        db: Session
    ) -> list[KnowledgeSourceRecord]:

        return self.repository.get_all(db)

    def delete_knowledge_source(
        self,
        db: Session,
        knowledge_source_id: int
    ) -> bool:

        knowledge_source = self.repository.get_by_id(
            db,
            knowledge_source_id
        )

        if knowledge_source is None:
            return False

        self.repository.delete(
            db,
            knowledge_source
        )

        return True