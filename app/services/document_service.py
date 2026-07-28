from sqlalchemy.orm import Session

from app.models.document import Document
from app.repositories.document_repository import DocumentRepository


class DocumentService:

    def __init__(self):
        self.repository = DocumentRepository()

    def create_document(
        self,
        db: Session,
        filename: str,
        file_type: str,
        file_path: str
    ) -> Document:

        document = Document(
            filename=filename,
            file_type=file_type,
            file_path=file_path,
            status="uploaded"
        )

        return self.repository.create(
            db,
            document
        )

    def get_document(
        self,
        db: Session,
        document_id: int
    ) -> Document | None:

        return self.repository.get_by_id(
            db,
            document_id
        )

    def get_documents(
        self,
        db: Session
    ) -> list[Document]:

        return self.repository.get_all(db)