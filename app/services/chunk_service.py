from app.chunkers.document_chunker import DocumentChunker
from app.repositories.document_chunk_repository import DocumentChunkRepository
from app.embeddings.embedding_generator import EmbeddingGenerator


class ChunkService:

    def __init__(
        self,
        chunker: DocumentChunker,
        repository: DocumentChunkRepository,
        embedding_generator: EmbeddingGenerator
    ):

        self.chunker = chunker
        self.repository = repository
        self.embedding_generator = embedding_generator


    def create_and_store_chunks(
        self,
        document_id: int,
        document_text: str
    ):

        chunks = self.chunker.chunk(
            document_text
        )

        texts = [
            chunk["content"]
            for chunk in chunks
        ]

        embeddings = self.embedding_generator.generate(
            texts
        )

        return self.repository.create(
            document_id=document_id,
            chunks=chunks,
            embeddings=embeddings
        )