from app.embeddings.embedding_generator import EmbeddingGenerator
from app.repositories.document_chunk_repository import (
    DocumentChunkRepository
)
from app.services.context_builder_service import (
    ContextBuilderService
)


class RetrievalService:

    def __init__(
        self,
        repository: DocumentChunkRepository,
        embedding_generator: EmbeddingGenerator,
        context_builder: ContextBuilderService,
        document_id: int | None = None,
        document_ids: list[int] | None = None
    ):

        if (
            document_id is not None
            and document_ids is not None
        ):
            raise ValueError(
                "Provide either document_id or document_ids, "
                "not both."
            )

        self.repository = repository
        self.embedding_generator = embedding_generator
        self.context_builder = context_builder
        self.document_id = document_id
        self.document_ids = document_ids

    def retrieve(
        self,
        question: str,
        limit: int = 5
    ) -> str:

        if not question.strip():
            raise ValueError(
                "Question cannot be empty."
            )

        query_embedding = self.embedding_generator.generate(
            [question]
        )[0]

        chunks = self.repository.find_similar(
            query_embedding=query_embedding,
            limit=limit,
            document_id=self.document_id,
            document_ids=self.document_ids
        )

        return self.context_builder.build_context(
            chunks
        )