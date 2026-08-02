from pathlib import Path

import yaml

from doc_generators.constants import (
    PROJECT_STATE_FILE
)


def load_project_state(
    root: Path
) -> dict:
    """
    Load project_state.yaml from project_manifest.

    The root argument is retained so existing generator calls
    remain compatible.
    """

    del root

    with PROJECT_STATE_FILE.open(
        "r",
        encoding="utf-8"
    ) as file:
        state = yaml.safe_load(file)

    if not isinstance(state, dict):
        raise ValueError(
            "project_state.yaml must contain a YAML mapping."
        )

    return state