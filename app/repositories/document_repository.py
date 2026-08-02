from sqlalchemy.orm import Session

from app.models.document import Document


class DocumentRepository:

    def create(
        self,
        db: Session,
        document: Document
    ) -> Document:

        db.add(document)
        db.commit()
        db.refresh(document)

        return document

    def get_by_id(
        self,
        db: Session,
        document_id: int
    ) -> Document | None:

        return (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

    def get_by_source_and_path(
        self,
        db: Session,
        knowledge_source_id: int,
        file_path: str
    ) -> Document | None:

        return (
            db.query(Document)
            .filter(
                Document.knowledge_source_id == knowledge_source_id,
                Document.file_path == file_path
            )
            .first()
        )

    def get_all(
        self,
        db: Session
    ) -> list[Document]:

        return (
            db.query(Document)
            .order_by(Document.id)
            .all()
        )

    def get_all_by_source(
        self,
        db: Session,
        knowledge_source_id: int
    ) -> list[Document]:

        return (
            db.query(Document)
            .filter(
                Document.knowledge_source_id == knowledge_source_id
            )
            .order_by(Document.file_path)
            .all()
        )

    def delete(
        self,
        db: Session,
        document: Document
    ) -> None:

        db.delete(document)
        db.commit()