from app.database import SessionLocal

from app.embeddings.embedding_generator import EmbeddingGenerator
from app.repositories.document_chunk_repository import (
    DocumentChunkRepository
)


def test_vector_similarity_search():

    question = (
        "What is EnterpriseBrain and what does it do?"
    )

    embedding_generator = EmbeddingGenerator()

    query_embedding = embedding_generator.generate(
        [question]
    )[0]

    db = SessionLocal()

    try:

        repository = DocumentChunkRepository(
            db
        )

        results = repository.find_similar(
            query_embedding=query_embedding,
            limit=5
        )

        print("\nVector Similarity Search Results\n")
        print(f"Question: {question}")
        print("-" * 50)

        if not results:
            print(
                "No embedded document chunks were found."
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
    test_vector_similarity_search()