from __future__ import annotations

import shutil
import subprocess
import sys
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]

STATE_DIRECTORY = (
    ROOT
    / "project_manifest"
    / "state"
)

PENDING_DIRECTORY = (
    ROOT
    / "project_manifest"
    / "updates"
    / "pending"
)

APPLIED_DIRECTORY = (
    ROOT
    / "project_manifest"
    / "updates"
    / "applied"
)

UPDATE_DOCS_SCRIPT = (
    ROOT
    / "tools"
    / "update_docs.py"
)


STATE_FILE_MAPPING = {
    "project": "project.yaml",
    "environment": "project.yaml",
    "last_updated": "project.yaml",
    "vision": "vision.yaml",
    "roadmap": "roadmap.yaml",
    "progress": "progress.yaml",
    "quality_backlog": "progress.yaml",
    "database": "database.yaml",
    "database_design": "database.yaml",
    "application_architecture": (
        "application_architecture.yaml"
    ),
    "architecture_decisions": (
        "application_architecture.yaml"
    ),
    "dependencies": "dependencies.yaml",
    "assistant_context": "assistant_context.yaml",
    "user_learning_preferences": (
        "user_learning_preferences.yaml"
    ),
    "documentation": "history.yaml",
    "changelog": "history.yaml",
}


def load_yaml(
    file_path: Path
) -> dict[str, Any]:

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
            f"Expected YAML mapping in: {file_path}"
        )

    return content


def write_yaml(
    file_path: Path,
    content: dict[str, Any]
) -> None:

    temporary_file = file_path.with_suffix(
        file_path.suffix + ".tmp"
    )

    with temporary_file.open(
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

    temporary_file.replace(
        file_path
    )


def find_pending_update() -> Path:

    pending_files = sorted(
        PENDING_DIRECTORY.glob("*.yaml")
    )

    if not pending_files:
        raise FileNotFoundError(
            "No pending project update YAML was found."
        )

    if len(pending_files) > 1:
        raise ValueError(
            "Only one pending project update is allowed. "
            f"Found: {[file.name for file in pending_files]}"
        )

    return pending_files[0]


def load_complete_state() -> dict[str, Any]:

    complete_state: dict[str, Any] = {}

    state_files = sorted(
        STATE_DIRECTORY.glob("*.yaml")
    )

    for state_file in state_files:
        if state_file.name == "state_index.yaml":
            continue

        content = load_yaml(
            state_file
        )

        for section_name, section_value in content.items():
            if section_name in complete_state:
                raise ValueError(
                    "Duplicate state section found: "
                    f"{section_name}"
                )

            complete_state[
                section_name
            ] = section_value

    return complete_state


def add_unique_items(
    target: list[Any],
    items: list[Any]
) -> None:

    for item in items:
        if item not in target:
            target.append(
                deepcopy(item)
            )


def apply_project_changes(
    state: dict[str, Any],
    update: dict[str, Any]
) -> None:

    project_update = update.get(
        "project",
        {}
    )

    if "version" in project_update:
        state["project"]["version"] = str(
            project_update["version"]
        )

    state["last_updated"] = (
        update["update"]["date"]
    )


def apply_progress_changes(
    state: dict[str, Any],
    update: dict[str, Any]
) -> None:

    progress_update = update.get(
        "progress",
        {}
    )

    progress_state = state[
        "progress"
    ]

    add_unique_items(
        progress_state["completed"],
        progress_update.get(
            "add_completed",
            []
        )
    )

    for field_name in (
        "phase",
        "current_step",
        "current_task",
        "next_task",
    ):
        if field_name in progress_update:
            progress_state[field_name] = (
                progress_update[field_name]
            )


def apply_vision_changes(
    state: dict[str, Any],
    update: dict[str, Any]
) -> None:

    vision_update = update.get(
        "vision",
        {}
    )

    vision_state = state[
        "vision"
    ]

    add_unique_items(
        vision_state["current_scope"],
        vision_update.get(
            "add_current_scope",
            []
        )
    )

    add_unique_items(
        vision_state["future_scope"],
        vision_update.get(
            "add_future_scope",
            []
        )
    )


def apply_architecture_changes(
    state: dict[str, Any],
    update: dict[str, Any]
) -> None:

    architecture_update = update.get(
        "architecture",
        {}
    )

    architecture_state = state[
        "application_architecture"
    ]

    add_unique_items(
        architecture_state["architecture_style"],
        architecture_update.get(
            "add_styles",
            []
        )
    )

    add_unique_items(
        architecture_state["layers"],
        architecture_update.get(
            "add_layers",
            []
        )
    )

    modules_update = architecture_update.get(
        "add_modules",
        {}
    )

    modules_state = architecture_state.setdefault(
        "modules",
        {}
    )

    for module_group, module_paths in (
        modules_update.items()
    ):
        target_modules = modules_state.setdefault(
            module_group,
            []
        )

        add_unique_items(
            target_modules,
            module_paths
        )


def apply_database_changes(
    state: dict[str, Any],
    update: dict[str, Any]
) -> None:

    database_update = update.get(
        "database",
        {}
    )

    database_state = state[
        "database"
    ]

    add_unique_items(
        database_state.setdefault(
            "schemas",
            []
        ),
        database_update.get(
            "add_schemas",
            []
        )
    )

    add_unique_items(
        database_state.setdefault(
            "tables",
            []
        ),
        database_update.get(
            "add_tables",
            []
        )
    )

    add_unique_items(
        database_state.setdefault(
            "future_tables",
            []
        ),
        database_update.get(
            "add_future_tables",
            []
        )
    )


def apply_changelog_changes(
    state: dict[str, Any],
    update: dict[str, Any]
) -> None:

    changelog_update = update.get(
        "changelog"
    )

    if not changelog_update:
        return

    changelog_state = state.setdefault(
        "changelog",
        {}
    )

    entry = {
        "version": str(
            changelog_update.get(
                "version",
                state["project"]["version"]
            )
        ),
        "date": str(
            changelog_update.get(
                "date",
                state["last_updated"]
            )
        ),
        "summary": changelog_update[
            "summary"
        ],
    }

    if isinstance(changelog_state, dict):
        entries = changelog_state.setdefault(
            "entries",
            []
        )

        if not isinstance(entries, list):
            raise ValueError(
                "changelog.entries must be a list."
            )

        if entry not in entries:
            entries.append(
                entry
            )

        return

    if isinstance(changelog_state, list):
        if entry not in changelog_state:
            changelog_state.append(
                entry
            )

        return

    raise ValueError(
        "The changelog section must be "
        "a mapping or a list."
    )

def apply_update(
    state: dict[str, Any],
    update: dict[str, Any]
) -> dict[str, Any]:

    if "update" not in update:
        raise ValueError(
            "Update YAML must contain an update section."
        )

    required_update_fields = {
        "id",
        "date",
        "description",
    }

    missing_fields = (
        required_update_fields
        - set(update["update"])
    )

    if missing_fields:
        raise ValueError(
            "Missing update fields: "
            f"{sorted(missing_fields)}"
        )

    updated_state = deepcopy(
        state
    )

    apply_project_changes(
        updated_state,
        update
    )

    apply_progress_changes(
        updated_state,
        update
    )

    apply_vision_changes(
        updated_state,
        update
    )

    apply_architecture_changes(
        updated_state,
        update
    )

    apply_database_changes(
        updated_state,
        update
    )

    apply_changelog_changes(
        updated_state,
        update
    )

    return updated_state


def split_state_by_file(
    state: dict[str, Any]
) -> dict[str, dict[str, Any]]:

    file_contents: dict[
        str,
        dict[str, Any]
    ] = {}

    for section_name, section_value in state.items():
        file_name = STATE_FILE_MAPPING.get(
            section_name
        )

        if file_name is None:
            file_name = "history.yaml"

        file_content = file_contents.setdefault(
            file_name,
            {}
        )

        file_content[
            section_name
        ] = section_value

    return file_contents


def validate_required_sections(
    state: dict[str, Any]
) -> None:

    required_sections = {
        "project",
        "vision",
        "roadmap",
        "progress",
        "database",
        "application_architecture",
        "dependencies",
        "assistant_context",
        "user_learning_preferences",
        "last_updated",
    }

    missing_sections = (
        required_sections
        - set(state)
    )

    if missing_sections:
        raise ValueError(
            "Updated project state is missing sections: "
            f"{sorted(missing_sections)}"
        )


def create_backups(
    state_files: dict[str, dict[str, Any]]
) -> dict[Path, Path]:

    backups: dict[
        Path,
        Path
    ] = {}

    for file_name in state_files:
        state_file = (
            STATE_DIRECTORY / file_name
        )

        backup_file = state_file.with_suffix(
            state_file.suffix + ".bak"
        )

        if state_file.exists():
            shutil.copy2(
                state_file,
                backup_file
            )

            backups[
                state_file
            ] = backup_file

    return backups


def restore_backups(
    backups: dict[Path, Path]
) -> None:

    for state_file, backup_file in backups.items():
        if backup_file.exists():
            shutil.copy2(
                backup_file,
                state_file
            )


def delete_backups(
    backups: dict[Path, Path]
) -> None:

    for backup_file in backups.values():
        backup_file.unlink(
            missing_ok=True
        )


def run_documentation_generator() -> None:

    result = subprocess.run(
        [
            sys.executable,
            str(UPDATE_DOCS_SCRIPT),
        ],
        cwd=ROOT,
        check=False
    )

    if result.returncode != 0:
        raise RuntimeError(
            "Documentation generation failed."
        )


def archive_update(
    pending_file: Path,
    update: dict[str, Any]
) -> Path:

    APPLIED_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True
    )

    update_id = str(
        update["update"]["id"]
    )

    update_date = str(
        update["update"]["date"]
    )

    safe_timestamp = datetime.now().strftime(
        "%H%M%S"
    )

    archive_name = (
        f"{update_date}_{safe_timestamp}_"
        f"{update_id}.yaml"
    )

    archive_path = (
        APPLIED_DIRECTORY / archive_name
    )

    shutil.move(
        str(pending_file),
        str(archive_path)
    )

    return archive_path


def main() -> None:

    print("=" * 60)
    print("EnterpriseBrain Project Update")
    print("=" * 60)
    print()

    pending_file = find_pending_update()

    print(
        f"Pending update: {pending_file.name}"
    )

    update = load_yaml(
        pending_file
    )

    current_state = load_complete_state()

    updated_state = apply_update(
        current_state,
        update
    )

    validate_required_sections(
        updated_state
    )

    state_files = split_state_by_file(
        updated_state
    )

    backups = create_backups(
        state_files
    )

    try:
        for file_name, file_content in (
            state_files.items()
        ):
            write_yaml(
                STATE_DIRECTORY / file_name,
                file_content
            )

        run_documentation_generator()

        archived_file = archive_update(
            pending_file,
            update
        )

    except Exception:
        restore_backups(
            backups
        )
        raise

    finally:
        delete_backups(
            backups
        )

    print()
    print(
        "Project state updated successfully."
    )
    print(
        "Documentation regenerated successfully."
    )
    print(
        f"Applied update archived as: "
        f"{archived_file.name}"
    )
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()