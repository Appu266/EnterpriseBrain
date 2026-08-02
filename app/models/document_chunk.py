from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    Integer,
    JSON,
    Text,
    UniqueConstraint,
    func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.document import Document


class DocumentChunk(Base):
    """
    Represents one searchable section of a document.

    A document is divided into ordered chunks so EnterpriseBrain can
    generate embeddings and retrieve only the most relevant sections.
    """

    __tablename__ = "document_chunks"

    __table_args__ = (
        UniqueConstraint(
            "document_id",
            "chunk_number",
            name="uq_document_chunks_document_number"
        ),
        Index(
            "ix_document_chunks_document_number",
            "document_id",
            "chunk_number"
        ),
        {
            "schema": "knowledge"
        }
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    document_id: Mapped[int] = mapped_column(
        ForeignKey(
            "knowledge.documents.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    chunk_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(768),
        nullable=True
    )

    chunk_metadata: Mapped[dict[str, Any] | None] = mapped_column(
        JSON,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    document: Mapped[Document] = relationship(
        back_populates="chunks"
    )