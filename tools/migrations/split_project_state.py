from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]

SOURCE_FILE = (
    ROOT
    / "project_manifest"
    / "project_state.yaml"
)

STATE_DIRECTORY = (
    ROOT
    / "project_manifest"
    / "state"
)

INDEX_FILE = (
    STATE_DIRECTORY
    / "state_index.yaml"
)


SECTION_MAPPING: dict[str, list[str]] = {
    "project.yaml": [
        "project",
        "environment",
        "last_updated",
    ],
    "vision.yaml": [
        "vision",
    ],
    "roadmap.yaml": [
        "roadmap",
    ],
    "progress.yaml": [
        "progress",
        "quality_backlog",
    ],
    "database.yaml": [
        "database",
        "database_design",
    ],
    "application_architecture.yaml": [
        "application_architecture",
        "architecture_decisions",
    ],
    "dependencies.yaml": [
        "dependencies",
    ],
    "assistant_context.yaml": [
        "assistant_context",
    ],
    "user_learning_preferences.yaml": [
        "user_learning_preferences",
    ],
    "history.yaml": [
        "documentation",
        "changelog",
    ],
}


def load_yaml(
    file_path: Path
) -> dict[str, Any]:
    """
    Load a YAML file containing a top-level mapping.
    """

    if not file_path.exists():
        raise FileNotFoundError(
            f"Required YAML file not found: {file_path}"
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


def write_yaml(
    file_path: Path,
    content: dict[str, Any]
) -> None:
    """
    Write a YAML mapping while preserving insertion order.
    """

    with file_path.open(
        "w",
        encoding="utf-8"
    ) as file:
        yaml.safe_dump(
            content,
            file,
            sort_keys=False,
            allow_unicode=True,
            width=100
        )


def split_state(
    original_state: dict[str, Any]
) -> tuple[
    dict[str, dict[str, Any]],
    list[str]
]:
    """
    Split the original project state into focused state files.

    Any section not explicitly mapped is preserved inside history.yaml.
    """

    state_files: dict[str, dict[str, Any]] = {}
    assigned_sections: set[str] = set()

    for file_name, section_names in (
        SECTION_MAPPING.items()
    ):
        file_content: dict[str, Any] = {}

        for section_name in section_names:
            if section_name not in original_state:
                continue

            file_content[section_name] = deepcopy(
                original_state[section_name]
            )

            assigned_sections.add(
                section_name
            )

        state_files[file_name] = file_content

    unassigned_sections = [
        section_name
        for section_name in original_state
        if section_name not in assigned_sections
    ]

    if unassigned_sections:
        history_content = state_files.setdefault(
            "history.yaml",
            {}
        )

        for section_name in unassigned_sections:
            history_content[section_name] = deepcopy(
                original_state[section_name]
            )

    return state_files, unassigned_sections


def build_index(
    original_state: dict[str, Any],
    state_files: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    """
    Build the index used to reconstruct the complete state.
    """

    section_to_file: dict[str, str] = {}

    for file_name, file_content in (
        state_files.items()
    ):
        for section_name in file_content:
            if section_name in section_to_file:
                raise ValueError(
                    "A section was assigned to multiple state files: "
                    f"{section_name}"
                )

            section_to_file[section_name] = file_name

    return {
        "format_version": 1,
        "legacy_source": "project_state.yaml",
        "top_level_section_order": list(
            original_state.keys()
        ),
        "section_to_file": section_to_file,
        "state_files": list(
            state_files.keys()
        ),
        "legacy_source_retained": True,
        "split_validation": "passed",
    }


def reconstruct_state(
    state_files: dict[str, dict[str, Any]],
    state_index: dict[str, Any]
) -> dict[str, Any]:
    """
    Reconstruct the original project state from split files.
    """

    loaded_sections: dict[str, Any] = {}

    for file_content in state_files.values():
        for section_name, section_value in (
            file_content.items()
        ):
            if section_name in loaded_sections:
                raise ValueError(
                    "Duplicate section found while reconstructing: "
                    f"{section_name}"
                )

            loaded_sections[section_name] = deepcopy(
                section_value
            )

    section_order = state_index[
        "top_level_section_order"
    ]

    missing_sections = [
        section_name
        for section_name in section_order
        if section_name not in loaded_sections
    ]

    if missing_sections:
        raise ValueError(
            "Sections missing during reconstruction: "
            f"{missing_sections}"
        )

    unexpected_sections = [
        section_name
        for section_name in loaded_sections
        if section_name not in section_order
    ]

    if unexpected_sections:
        raise ValueError(
            "Unexpected sections found during reconstruction: "
            f"{unexpected_sections}"
        )

    return {
        section_name: loaded_sections[
            section_name
        ]
        for section_name in section_order
    }


def validate_equal(
    original_state: dict[str, Any],
    reconstructed_state: dict[str, Any]
) -> None:
    """
    Fail if any section or value changed during splitting.
    """

    if original_state == reconstructed_state:
        return

    original_sections = set(
        original_state
    )

    reconstructed_sections = set(
        reconstructed_state
    )

    missing_sections = sorted(
        original_sections - reconstructed_sections
    )

    extra_sections = sorted(
        reconstructed_sections - original_sections
    )

    changed_sections = sorted(
        section_name
        for section_name in (
            original_sections
            & reconstructed_sections
        )
        if original_state[section_name]
        != reconstructed_state[section_name]
    )

    raise ValueError(
        "Project-state split validation failed.\n"
        f"Missing sections: {missing_sections}\n"
        f"Extra sections: {extra_sections}\n"
        f"Changed sections: {changed_sections}"
    )


def verify_written_files(
    original_state: dict[str, Any],
    state_index: dict[str, Any]
) -> None:
    """
    Reload written files from disk and validate them again.
    """

    written_state_files: dict[
        str,
        dict[str, Any]
    ] = {}

    for file_name in state_index[
        "state_files"
    ]:
        written_state_files[file_name] = load_yaml(
            STATE_DIRECTORY / file_name
        )

    reconstructed_state = reconstruct_state(
        state_files=written_state_files,
        state_index=state_index
    )

    validate_equal(
        original_state=original_state,
        reconstructed_state=reconstructed_state
    )


def main() -> None:
    print("=" * 60)
    print("EnterpriseBrain Project State Split")
    print("=" * 60)
    print()

    original_state = load_yaml(
        SOURCE_FILE
    )

    if not original_state:
        raise ValueError(
            "project_state.yaml is empty."
        )

    state_files, unassigned_sections = split_state(
        original_state
    )

    state_index = build_index(
        original_state=original_state,
        state_files=state_files
    )

    reconstructed_state = reconstruct_state(
        state_files=state_files,
        state_index=state_index
    )

    validate_equal(
        original_state=original_state,
        reconstructed_state=reconstructed_state
    )

    STATE_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True
    )

    for file_name, file_content in (
        state_files.items()
    ):
        write_yaml(
            STATE_DIRECTORY / file_name,
            file_content
        )

    write_yaml(
        INDEX_FILE,
        state_index
    )

    verify_written_files(
        original_state=original_state,
        state_index=state_index
    )

    print(
        f"Original top-level sections: "
        f"{len(original_state)}"
    )

    print(
        f"State files created: "
        f"{len(state_files)}"
    )

    for file_name, file_content in (
        state_files.items()
    ):
        print(
            f"  {file_name}: "
            f"{len(file_content)} section(s)"
        )

    if unassigned_sections:
        print()
        print(
            "Unmapped sections safely preserved "
            "inside history.yaml:"
        )

        for section_name in unassigned_sections:
            print(
                f"  - {section_name}"
            )

    print()
    print(
        "Deep equality validation passed."
    )
    print(
        "No project history or configuration was lost."
    )
    print(
        "The original project_state.yaml remains unchanged."
    )
    print()
    print("=" * 60)
    print("Project state split completed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()