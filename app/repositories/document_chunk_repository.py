from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk


class DocumentChunkRepository:

    def __init__(
        self,
        db: Session
    ):
        self.db = db

    def create(
        self,
        document_id: int,
        chunks: list[dict],
        embeddings: list[list[float]]
    ):

        document_chunks = []

        for chunk, embedding in zip(
            chunks,
            embeddings
        ):

            document_chunk = DocumentChunk(
                document_id=document_id,
                chunk_number=chunk["chunk_number"],
                content=chunk["content"],
                embedding=embedding
            )

            document_chunks.append(
                document_chunk
            )

        self.db.add_all(
            document_chunks
        )

        self.db.commit()

        return document_chunks

    def find_similar(
        self,
        query_embedding: list[float],
        limit: int = 5,
        document_id: int | None = None,
        document_ids: list[int] | None = None
    ) -> list[tuple[DocumentChunk, float]]:

        if (
            document_id is not None
            and document_ids is not None
        ):
            raise ValueError(
                "Provide either document_id or document_ids, "
                "not both."
            )

        if document_ids is not None and not document_ids:
            return []

        distance = DocumentChunk.embedding.cosine_distance(
            query_embedding
        ).label("distance")

        statement = select(
            DocumentChunk,
            distance
        ).where(
            DocumentChunk.embedding.is_not(None)
        )

        if document_id is not None:
            statement = statement.where(
                DocumentChunk.document_id == document_id
            )

        if document_ids is not None:
            statement = statement.where(
                DocumentChunk.document_id.in_(
                    document_ids
                )
            )

        statement = (
            statement
            .order_by(distance)
            .limit(limit)
        )

        return self.db.execute(
            statement
        ).all()