from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Integer,
    String
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class KnowledgeSourceRecord(Base):
    """
    Persistent database record for one EnterpriseBrain knowledge source.

    A knowledge source may represent a local document, local folder,
    Git repository, Confluence space, Jira project, SharePoint location,
    database, or another future connector.
    """

    __tablename__ = "knowledge_sources"

    __table_args__ = {
        "schema": "knowledge"
    }

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
        nullable=False
    )

    location: Mapped[str] = mapped_column(
        String(1000),
        nullable=False
    )

    indexing_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="registered"
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    document_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    chunk_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    last_indexed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )