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


    def get_all(
        self,
        db: Session
    ) -> list[Document]:

        return (
            db.query(Document)
            .all()
        )


    def delete(
        self,
        db: Session,
        document: Document
    ) -> None:

        db.delete(document)
        db.commit()