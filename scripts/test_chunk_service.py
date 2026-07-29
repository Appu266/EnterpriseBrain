from app.database import SessionLocal

from app.models.document import Document
from app.models.document_chunk import DocumentChunk

from app.chunkers.document_chunker import DocumentChunker
from app.repositories.document_chunk_repository import DocumentChunkRepository
from app.services.chunk_service import ChunkService
from app.embeddings.embedding_generator import EmbeddingGenerator


def test_chunk_service():

    db = SessionLocal()

    try:

        document_id = 1

        document_text = """
        EnterpriseBrain is an AI-powered Enterprise Knowledge Assistant.

        It understands enterprise documents and helps users
        retrieve information using artificial intelligence.

        This document explains the initial capabilities of the system.
        """

        chunker = DocumentChunker(
            chunk_size=10
        )

        repository = DocumentChunkRepository(
            db
        )

        embedding_generator = EmbeddingGenerator()

        service = ChunkService(
            chunker,
            repository,
            embedding_generator
        )

        chunks = service.create_and_store_chunks(
            document_id=document_id,
            document_text=document_text
        )

        print("\nChunks stored successfully\n")

        for chunk in chunks:
            print(
                f"Chunk ID: {chunk.id}, "
                f"Chunk Number: {chunk.chunk_number}"
            )
            print(chunk.content)
            print("-" * 50)

    finally:

        db.close()


if __name__ == "__main__":
    test_chunk_service()