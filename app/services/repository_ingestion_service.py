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
from app.services.indexing_run_service import IndexingRunService
from app.services.knowledge_source_service import KnowledgeSourceService
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

    The repository is registered as a persistent knowledge source.
    Every ingestion attempt is tracked as an indexing run, while each
    supported repository file is stored as a document.
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

        repository_name = source_files[0].repository_name
        repository_location = str(repository_root)

        knowledge_source_service = KnowledgeSourceService()
        indexing_run_service = IndexingRunService()
        document_service = DocumentService()

        persistent_source = (
            knowledge_source_service
            .get_knowledge_source_by_type_and_location(
                db=self.db,
                source_type=KnowledgeSourceType.GIT_REPOSITORY.value,
                location=repository_location
            )
        )

        if persistent_source is None:
            persistent_source = (
                knowledge_source_service.create_knowledge_source(
                    db=self.db,
                    name=repository_name,
                    source_type=(
                        KnowledgeSourceType.GIT_REPOSITORY.value
                    ),
                    location=repository_location
                )
            )

        indexing_run = indexing_run_service.start_indexing_run(
            db=self.db,
            knowledge_source_id=persistent_source.id
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

        file_results: list[RepositoryFileIngestionResult] = []
        document_ids: list[int] = []
        total_stored_chunks = 0

        try:
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

                stored_document = (
                    document_service.create_document(
                        db=self.db,
                        knowledge_source_id=persistent_source.id,
                        indexing_run_id=indexing_run.id,
                        filename=processing_document.file_name,
                        file_type=file_type,
                        file_path=relative_path,
                        status="processing"
                    )
                )

                stored_chunks = (
                    chunk_service.create_and_store_chunks(
                        document_id=stored_document.id,
                        document_text=processing_document.content
                    )
                )

                stored_document.status = "indexed"
                self.db.commit()
                self.db.refresh(stored_document)

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

            indexing_run_service.complete_indexing_run(
                db=self.db,
                indexing_run_id=indexing_run.id,
                documents_discovered=len(source_files),
                documents_processed=len(file_results),
                documents_failed=0,
                chunks_created=total_stored_chunks
            )

        except Exception as error:
            self.db.rollback()

            indexing_run_service.fail_indexing_run(
                db=self.db,
                indexing_run_id=indexing_run.id,
                error_message=str(error),
                documents_discovered=len(source_files),
                documents_processed=len(file_results),
                documents_failed=1,
                chunks_created=total_stored_chunks
            )

            raise

        knowledge_source = KnowledgeSource(
            name=repository_name,
            source_type=KnowledgeSourceType.GIT_REPOSITORY,
            location=repository_location,
            metadata={
                "knowledge_source_id": persistent_source.id,
                "indexing_run_id": indexing_run.id,
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
            repository_root=repository_location,
            discovered_file_count=len(source_files),
            ingested_file_count=len(file_results),
            stored_chunk_count=total_stored_chunks,
            files=file_results,
            context=repository_context
        )