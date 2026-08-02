from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session

from app.chunkers.document_chunker import DocumentChunker
from app.embeddings.embedding_generator import EmbeddingGenerator
from app.models.knowledge_source import (
    KnowledgeSource,
    KnowledgeSourceType
)
from app.models.repository_ingestion_context import (
    RepositoryIngestionContext
)
from app.repositories.document_chunk_repository import (
    DocumentChunkRepository
)
from app.services.chunk_service import ChunkService
from app.services.document_service import DocumentService
from app.services.repository_discovery_service import (
    RepositoryDiscoveryService
)
from app.services.repository_reader_service import (
    RepositoryReaderService
)


@dataclass(frozen=True)
class RepositoryFileIngestionResult:
    document_id: int
    file_name: str
    relative_path: str
    file_type: str
    stored_chunk_count: int
    metadata: dict[str, Any] = field(
        default_factory=dict
    )


@dataclass(frozen=True)
class RepositoryIngestionResult:
    repository_name: str
    repository_root: str
    discovered_file_count: int
    ingested_file_count: int
    stored_chunk_count: int
    files: list[RepositoryFileIngestionResult]
    context: RepositoryIngestionContext


class RepositoryIngestionService:
    """
    Discovers, reads and stores supported files from a repository.

    The repository is represented as a generic KnowledgeSource,
    while each supported repository file is stored as a document.
    """

    def __init__(
        self,
        db: Session,
        embedding_generator: EmbeddingGenerator,
        discovery_service: RepositoryDiscoveryService | None = None,
        reader_service: RepositoryReaderService | None = None,
        storage_chunk_size: int = 500
    ):
        self.db = db
        self.embedding_generator = embedding_generator

        self.discovery_service = (
            discovery_service
            or RepositoryDiscoveryService()
        )

        self.reader_service = (
            reader_service
            or RepositoryReaderService()
        )

        self.storage_chunk_size = storage_chunk_size

    def ingest(
        self,
        repository_path: str | Path
    ) -> RepositoryIngestionResult:

        repository_root = Path(
            repository_path
        ).expanduser().resolve()

        source_files = self.discovery_service.discover(
            repository_root
        )

        if not source_files:
            raise ValueError(
                "No supported source files were found "
                f"in repository: {repository_root}"
            )

        processing_documents = self.reader_service.read_all(
            source_files
        )

        document_service = DocumentService()

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

        file_results = []
        document_ids = []
        total_stored_chunks = 0

        for processing_document in processing_documents:
            metadata = processing_document.metadata

            relative_path = metadata.get(
                "relative_path",
                processing_document.file_name
            )

            extension = metadata.get(
                "extension",
                Path(
                    processing_document.file_name
                ).suffix.lower()
            )

            file_type = extension.lstrip(".").upper()

            stored_document = document_service.create_document(
                db=self.db,
                filename=processing_document.file_name,
                file_type=file_type,
                file_path=relative_path
            )

            stored_chunks = chunk_service.create_and_store_chunks(
                document_id=stored_document.id,
                document_text=processing_document.content
            )

            stored_chunk_count = len(
                stored_chunks
            )

            document_ids.append(
                stored_document.id
            )

            total_stored_chunks += stored_chunk_count

            file_results.append(
                RepositoryFileIngestionResult(
                    document_id=stored_document.id,
                    file_name=processing_document.file_name,
                    relative_path=relative_path,
                    file_type=file_type,
                    stored_chunk_count=stored_chunk_count,
                    metadata=dict(metadata)
                )
            )

        repository_name = source_files[0].repository_name

        knowledge_source = KnowledgeSource(
            name=repository_name,
            source_type=KnowledgeSourceType.GIT_REPOSITORY,
            location=str(repository_root),
            metadata={
                "source_category": source_files[0].source_type,
                "discovered_file_count": len(source_files),
                "ingested_file_count": len(file_results),
                "stored_chunk_count": total_stored_chunks,
            }
        )

        repository_context = RepositoryIngestionContext(
            source=knowledge_source,
            document_ids=document_ids,
            metadata={
                "file_extensions": sorted({
                    source_file.extension
                    for source_file in source_files
                })
            }
        )

        return RepositoryIngestionResult(
            repository_name=repository_name,
            repository_root=str(repository_root),
            discovered_file_count=len(source_files),
            ingested_file_count=len(file_results),
            stored_chunk_count=total_stored_chunks,
            files=file_results,
            context=repository_context
        )