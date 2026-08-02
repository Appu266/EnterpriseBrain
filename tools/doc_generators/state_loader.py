from pathlib import Path
from typing import Any

import yaml

from doc_generators.constants import (
    PROJECT_MANIFEST_DIR
)


STATE_DIRECTORY = (
    PROJECT_MANIFEST_DIR / "state"
)

STATE_INDEX_FILE = (
    STATE_DIRECTORY / "state_index.yaml"
)


def load_yaml(
    file_path: Path
) -> dict[str, Any]:
    """
    Load a YAML file containing a top-level mapping.
    """

    if not file_path.exists():
        raise FileNotFoundError(
            f"Required state file not found: {file_path}"
        )

    with file_path.open(
        "r",
        encoding="utf-8"
    ) as file:
        content = yaml.safe_load(file)

    if content is None:
        return {}

    if not isinstance(content, dict):
        raise ValueError(
            f"Expected a YAML mapping in: {file_path}"
        )

    return content


def load_project_state_from_files() -> dict[str, Any]:
    """
    Reconstruct the complete EnterpriseBrain project state
    from the split YAML files inside project_manifest/state.
    """

    state_index = load_yaml(
        STATE_INDEX_FILE
    )

    state_files = state_index.get(
        "state_files"
    )

    section_order = state_index.get(
        "top_level_section_order"
    )

    if not isinstance(state_files, list):
        raise ValueError(
            "state_index.yaml must contain "
            "a state_files list."
        )

    if not isinstance(section_order, list):
        raise ValueError(
            "state_index.yaml must contain "
            "a top_level_section_order list."
        )

    loaded_sections: dict[str, Any] = {}

    for file_name in state_files:
        if not isinstance(file_name, str):
            raise ValueError(
                "Every state file name must be a string."
            )

        state_file = (
            STATE_DIRECTORY / file_name
        )

        state_content = load_yaml(
            state_file
        )

        for section_name, section_value in (
            state_content.items()
        ):
            if section_name in loaded_sections:
                raise ValueError(
                    "Duplicate top-level section found: "
                    f"{section_name}"
                )

            loaded_sections[
                section_name
            ] = section_value

    missing_sections = [
        section_name
        for section_name in section_order
        if section_name not in loaded_sections
    ]

    if missing_sections:
        raise ValueError(
            "Missing project-state sections: "
            f"{missing_sections}"
        )

    unexpected_sections = [
        section_name
        for section_name in loaded_sections
        if section_name not in section_order
    ]

    if unexpected_sections:
        raise ValueError(
            "Unexpected project-state sections: "
            f"{unexpected_sections}"
        )

    return {
        section_name: loaded_sections[
            section_name
        ]
        for section_name in section_order
    }