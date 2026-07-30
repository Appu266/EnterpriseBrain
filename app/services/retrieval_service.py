from app.embeddings.embedding_generator import EmbeddingGenerator
from app.repositories.document_chunk_repository import (
    DocumentChunkRepository
)


class RetrievalService:

    def __init__(
        self,
        repository: DocumentChunkRepository,
        embedding_generator: EmbeddingGenerator
    ):

        self.repository = repository
        self.embedding_generator = embedding_generator

    def retrieve(
        self,
        question: str,
        limit: int = 5
    ):

        if not question.strip():
            raise ValueError(
                "Question cannot be empty."
            )

        query_embedding = self.embedding_generator.generate(
            [question]
        )[0]

        return self.repository.find_similar(
            query_embedding=query_embedding,
            limit=limit
        )