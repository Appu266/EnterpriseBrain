from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    Integer,
    String,
    UniqueConstraint,
    func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.document import Document
    from app.models.indexing_run import IndexingRun


class KnowledgeSourceRecord(Base):
    """
    Persistent record representing one source of enterprise knowledge.

    Examples:
    - Git repository
    - Local folder
    - Individual file
    - Confluence space
    - Jira project
    - Database
    """

    __tablename__ = "knowledge_sources"

    __table_args__ = (
        UniqueConstraint(
            "source_type",
            "location",
            name="uq_knowledge_sources_type_location"
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

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    source_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True
    )

    location: Mapped[str] = mapped_column(
        String(1000),
        nullable=False
    )

    indexing_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="registered",
        index=True
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        index=True
    )

    last_indexed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
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

    indexing_runs: Mapped[list[IndexingRun]] = relationship(
        back_populates="knowledge_source",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    documents: Mapped[list[Document]] = relationship(
        back_populates="knowledge_source",
        cascade="all, delete-orphan",
        passive_deletes=True
    )