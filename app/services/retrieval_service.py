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
        context_builder: ContextBuilderService
    ):

        self.repository = repository
        self.embedding_generator = embedding_generator
        self.context_builder = context_builder


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
            limit=limit
        )

        return self.context_builder.build_context(
            chunks
        )