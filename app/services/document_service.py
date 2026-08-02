from sqlalchemy.orm import Session

from app.models.document import Document
from app.repositories.document_repository import DocumentRepository


class DocumentService:

    def __init__(self):
        self.repository = DocumentRepository()

    def create_document(
        self,
        db: Session,
        knowledge_source_id: int,
        filename: str,
        file_type: str,
        file_path: str,
        indexing_run_id: int | None = None,
        content_hash: str | None = None,
        status: str = "discovered"
    ) -> Document:

        existing_document = self.repository.get_by_source_and_path(
            db,
            knowledge_source_id,
            file_path
        )

        if existing_document is not None:
            raise ValueError(
                "A document with this file path is already registered "
                "for the knowledge source."
            )

        document = Document(
            knowledge_source_id=knowledge_source_id,
            indexing_run_id=indexing_run_id,
            filename=filename,
            file_type=file_type,
            file_path=file_path,
            content_hash=content_hash,
            status=status
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

    def get_document_by_source_and_path(
        self,
        db: Session,
        knowledge_source_id: int,
        file_path: str
    ) -> Document | None:

        return self.repository.get_by_source_and_path(
            db,
            knowledge_source_id,
            file_path
        )

    def get_documents(
        self,
        db: Session
    ) -> list[Document]:

        return self.repository.get_all(db)

    def get_documents_by_source(
        self,
        db: Session,
        knowledge_source_id: int
    ) -> list[Document]:

        return self.repository.get_all_by_source(
            db,
            knowledge_source_id
        )

    def delete_document(
        self,
        db: Session,
        document_id: int
    ) -> bool:

        document = self.repository.get_by_id(
            db,
            document_id
        )

        if document is None:
            return False

        self.repository.delete(
            db,
            document
        )

        return True