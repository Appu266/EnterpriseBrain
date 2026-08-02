from dataclasses import dataclass
from pathlib import Path

from sqlalchemy.orm import Session

from app.chunkers.document_chunker import DocumentChunker
from app.chunkers.text_chunker import TextChunker
from app.embeddings.embedding_generator import EmbeddingGenerator
from app.ingestion.document_loader import DocumentLoader
from app.llm.base_llm import BaseLLM
from app.readers.base_reader import BaseReader
from app.repositories.document_chunk_repository import (
    DocumentChunkRepository
)
from app.services.chunk_service import ChunkService
from app.services.context_builder_service import (
    ContextBuilderService
)
from app.services.document_service import DocumentService
from app.services.indexing_run_service import IndexingRunService
from app.services.knowledge_source_service import KnowledgeSourceService
from app.services.qa_service import QAResult, QAService
from app.services.retrieval_service import RetrievalService


@dataclass(frozen=True)
class DocumentIngestionResult:
    document_id: int
    file_name: str
    file_path: str
    stored_chunk_count: int


class DocumentAssistantService:

    def __init__(
        self,
        db: Session,
        reader: BaseReader,
        llm: BaseLLM,
        embedding_generator: EmbeddingGenerator,
        ingestion_chunk_size: int = 1000,
        storage_chunk_size: int = 500
    ):
        self.db = db
        self.reader = reader
        self.llm = llm
        self.embedding_generator = embedding_generator
        self.ingestion_chunk_size = ingestion_chunk_size
        self.storage_chunk_size = storage_chunk_size

        self._qa_service: QAService | None = None
        self._active_document_id: int | None = None
        self._active_document_name: str | None = None

    @property
    def has_active_document(self) -> bool:
        return self._qa_service is not None

    @property
    def active_document_id(self) -> int | None:
        return self._active_document_id

    @property
    def active_document_name(self) -> str | None:
        return self._active_document_name

    def ingest_document(
        self,
        file_path: str | Path
    ) -> DocumentIngestionResult:

        normalized_path = str(
            Path(file_path).expanduser().resolve()
        )

        document_loader = DocumentLoader(
            reader=self.reader,
            chunker=TextChunker(
                chunk_size=self.ingestion_chunk_size
            )
        )

        processing_document = document_loader.load(
            normalized_path
        )

        knowledge_source_service = KnowledgeSourceService()
        indexing_run_service = IndexingRunService()
        document_service = DocumentService()

        knowledge_source = (
            knowledge_source_service
            .get_knowledge_source_by_type_and_location(
                db=self.db,
                source_type="local_file",
                location=normalized_path
            )
        )

        if knowledge_source is None:
            knowledge_source = (
                knowledge_source_service.create_knowledge_source(
                    db=self.db,
                    name=processing_document.file_name,
                    source_type="local_file",
                    location=normalized_path
                )
            )

        indexing_run = indexing_run_service.start_indexing_run(
            db=self.db,
            knowledge_source_id=knowledge_source.id
        )

        try:
            stored_document = document_service.create_document(
                db=self.db,
                knowledge_source_id=knowledge_source.id,
                indexing_run_id=indexing_run.id,
                filename=processing_document.file_name,
                file_type=processing_document.metadata["file_type"],
                file_path=processing_document.file_path,
                status="processing"
            )

            chunk_repository = DocumentChunkRepository(
                self.db
            )

            chunk_service = ChunkService(
                chunker=DocumentChunker(
                    chunk_size=self.storage_chunk_size
                ),
                repository=chunk_repository,
                embedding_generator=self.embedding_generator
            )

            stored_chunks = chunk_service.create_and_store_chunks(
                document_id=stored_document.id,
                document_text=processing_document.content
            )

            stored_document.status = "indexed"
            self.db.commit()
            self.db.refresh(stored_document)

            indexing_run_service.complete_indexing_run(
                db=self.db,
                indexing_run_id=indexing_run.id,
                documents_discovered=1,
                documents_processed=1,
                documents_failed=0,
                chunks_created=len(stored_chunks)
            )

            retrieval_service = RetrievalService(
                repository=chunk_repository,
                embedding_generator=self.embedding_generator,
                context_builder=ContextBuilderService(),
                document_id=stored_document.id
            )

            self._qa_service = QAService(
                retrieval_service=retrieval_service,
                llm=self.llm
            )

            self._active_document_id = stored_document.id
            self._active_document_name = (
                processing_document.file_name
            )

            return DocumentIngestionResult(
                document_id=stored_document.id,
                file_name=processing_document.file_name,
                file_path=processing_document.file_path,
                stored_chunk_count=len(stored_chunks)
            )

        except Exception as error:
            self.db.rollback()

            indexing_run_service.fail_indexing_run(
                db=self.db,
                indexing_run_id=indexing_run.id,
                error_message=str(error),
                documents_discovered=1,
                documents_processed=0,
                documents_failed=1,
                chunks_created=0
            )

            raise

    def ask(
        self,
        question: str,
        conversation_history: list[dict[str, str]] | None = None
    ) -> QAResult:

        normalized_question = question.strip()

        if not normalized_question:
            raise ValueError(
                "Question cannot be empty."
            )

        if self._qa_service is None:
            raise RuntimeError(
                "No document has been ingested."
            )

        return self._qa_service.answer_with_context(
            question=normalized_question,
            conversation_history=conversation_history
        )

    def answer_question(
        self,
        question: str,
        conversation_history: list[dict[str, str]] | None = None
    ) -> QAResult:

        return self.ask(
            question=question,
            conversation_history=conversation_history
        )

    def close_document(self) -> None:
        self._qa_service = None
        self._active_document_id = None
        self._active_document_name = None