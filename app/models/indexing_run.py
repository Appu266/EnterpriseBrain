from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.document import Document
    from app.models.knowledge_source_record import KnowledgeSourceRecord


class IndexingRun(Base):
    """
    Represents one indexing attempt for a knowledge source.

    A knowledge source can have multiple indexing runs over time,
    allowing EnterpriseBrain to track indexing history, statistics,
    and failures.
    """

    __tablename__ = "indexing_runs"

    __table_args__ = (
        CheckConstraint(
            "documents_discovered >= 0",
            name="ck_indexing_runs_documents_discovered"
        ),
        CheckConstraint(
            "documents_processed >= 0",
            name="ck_indexing_runs_documents_processed"
        ),
        CheckConstraint(
            "documents_failed >= 0",
            name="ck_indexing_runs_documents_failed"
        ),
        CheckConstraint(
            "chunks_created >= 0",
            name="ck_indexing_runs_chunks_created"
        ),
        Index(
            "ix_indexing_runs_source_status",
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

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="running",
        index=True
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    documents_discovered: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    documents_processed: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    documents_failed: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    chunks_created: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
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

    knowledge_source: Mapped[KnowledgeSourceRecord] = relationship(
        back_populates="indexing_runs"
    )

    documents: Mapped[list[Document]] = relationship(
        back_populates="indexing_run",
        passive_deletes=True
    )