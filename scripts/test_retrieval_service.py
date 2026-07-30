from app.database import SessionLocal

from app.embeddings.embedding_generator import EmbeddingGenerator
from app.repositories.document_chunk_repository import (
    DocumentChunkRepository
)
from app.services.retrieval_service import RetrievalService


def test_retrieval_service():

    question = (
        "What is EnterpriseBrain and what does it do?"
    )

    db = SessionLocal()

    try:

        repository = DocumentChunkRepository(
            db
        )

        embedding_generator = EmbeddingGenerator()

        retrieval_service = RetrievalService(
            repository=repository,
            embedding_generator=embedding_generator
        )

        results = retrieval_service.retrieve(
            question=question,
            limit=5
        )

        print("\nRetrieval Service Results\n")
        print(f"Question: {question}")
        print("-" * 50)

        if not results:
            print(
                "No relevant document chunks were found."
            )
            return

        for chunk, distance in results:
            print(
                f"Chunk ID: {chunk.id}, "
                f"Document ID: {chunk.document_id}, "
                f"Chunk Number: {chunk.chunk_number}"
            )
            print(f"Cosine Distance: {distance:.4f}")
            print(f"Content: {chunk.content}")
            print("-" * 50)

    finally:

        db.close()


if __name__ == "__main__":
    test_retrieval_service()