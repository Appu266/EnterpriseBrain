from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.document_chunk import DocumentChunk
    from app.models.indexing_run import IndexingRun
    from app.models.knowledge_source_record import KnowledgeSourceRecord


class Document(Base):
    """
    Represents one file or logical document discovered within a
    knowledge source.

    Examples:
    - A SQL file inside a Git repository
    - A PDF inside a local folder
    - A future Jira issue or Confluence page
    """

    __tablename__ = "documents"

    __table_args__ = (
        UniqueConstraint(
            "knowledge_source_id",
            "file_path",
            name="uq_documents_source_file_path"
        ),
        Index(
            "ix_documents_source_status",
            "knowledge_source_id",
            "status"
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

    knowledge_source_id: Mapped[int] = mapped_column(
        ForeignKey(
            "knowledge.knowledge_sources.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    indexing_run_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "knowledge.indexing_runs.id",
            ondelete="SET NULL"
        ),
        nullable=True,
        index=True
    )

    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    file_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True
    )

    file_path: Mapped[str] = mapped_column(
        String(1000),
        nullable=False
    )

    content_hash: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
        index=True
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="discovered",
        index=True
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )

    knowledge_source: Mapped[KnowledgeSourceRecord] = relationship(
        back_populates="documents"
    )

    indexing_run: Mapped[IndexingRun | None] = relationship(
        back_populates="documents"
    )

    chunks: Mapped[list[DocumentChunk]] = relationship(
        back_populates="document",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="DocumentChunk.chunk_number"
    )