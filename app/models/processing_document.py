from dataclasses import dataclass, field
from typing import Any


@dataclass
class ProcessingDocument:
    """
    Represents a document while it flows through the EnterpriseBrain
    processing pipeline.

    This is NOT a database model.
    It exists only in memory during processing.
    """

    file_name: str
    file_path: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
    chunks: list[str] = field(default_factory=list)