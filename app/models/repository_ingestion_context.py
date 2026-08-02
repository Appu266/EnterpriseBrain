from dataclasses import dataclass, field
from typing import Any

from app.models.knowledge_source import KnowledgeSource


@dataclass(frozen=True)
class RepositoryIngestionContext:
    """
    Represents one ingested repository and the documents created from it.

    Repository-specific retrieval currently uses this context, while the
    generic KnowledgeSource model identifies the source itself.
    """

    source: KnowledgeSource
    document_ids: list[int]
    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    @property
    def repository_name(self) -> str:
        return self.source.name

    @property
    def repository_root(self) -> str:
        return self.source.location

    @property
    def document_count(self) -> int:
        return len(
            self.document_ids
        )

    @property
    def is_empty(self) -> bool:
        return not self.document_ids