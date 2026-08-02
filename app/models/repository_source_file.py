from dataclasses import dataclass, field
from typing import Any


@dataclass
class RepositorySourceFile:
    """
    Represents one source file discovered inside a repository.

    This is an in-memory model used during repository discovery
    and ingestion. It is not a database ORM model.
    """

    repository_name: str
    repository_root: str
    file_name: str
    relative_path: str
    absolute_path: str
    extension: str
    source_type: str
    content: str = ""
    metadata: dict[str, Any] = field(
        default_factory=dict
    )