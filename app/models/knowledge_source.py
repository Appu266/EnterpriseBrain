from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class KnowledgeSourceType(str, Enum):
    """
    Identifies the origin of knowledge ingested by EnterpriseBrain.
    """

    LOCAL_DOCUMENT = "local_document"
    LOCAL_FOLDER = "local_folder"
    GIT_REPOSITORY = "git_repository"
    CONFLUENCE = "confluence"
    JIRA = "jira"
    SHAREPOINT = "sharepoint"
    DATABASE = "database"
    S3 = "s3"


@dataclass(frozen=True)
class KnowledgeSource:
    """
    Represents a generic source of enterprise knowledge.

    A knowledge source may produce one document or many documents.
    This is currently an in-memory model and not a database ORM model.
    """

    name: str
    source_type: KnowledgeSourceType
    location: str
    metadata: dict[str, Any] = field(
        default_factory=dict
    )