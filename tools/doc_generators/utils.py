from pathlib import Path

from doc_generators.state_loader import (
    load_project_state_from_files
)


def load_project_state(
    root: Path
) -> dict:
    """
    Load the complete project state from split YAML files.

    The root argument is retained for compatibility with the
    existing documentation generator interface.
    """

    del root

    return load_project_state_from_files()