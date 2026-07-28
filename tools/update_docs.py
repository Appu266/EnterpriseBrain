from pathlib import Path
import yaml
from datetime import datetime


ROOT = Path(__file__).parent.parent


# ---------------------------------
# Load project state
# ---------------------------------

with open(ROOT / "project_state.yaml", "r", encoding="utf-8") as f:
    state = yaml.safe_load(f)


project = state["project"]
progress = state["progress"]


# ---------------------------------
# Generate PROJECT_STATUS.md
# ---------------------------------

completed = "\n".join(
    f"- [x] {item}" for item in progress["completed"]
)

project_status = f"""# EnterpriseBrain - Project Status

## Current Phase
{progress["phase"]}

## Current Step
{progress["current_step"]}

## Completed

{completed}

## Current Task
{progress["current_task"]}

## Next Task
{progress["next_task"]}

Last Updated: {state["last_updated"]}
"""

(ROOT / "PROJECT_STATUS.md").write_text(
    project_status,
    encoding="utf-8"
)


# ---------------------------------
# Generate MENTOR_CONTEXT.md
# ---------------------------------

mentor_context = f"""# EnterpriseBrain - Mentor Context

Project Version:
{project["version"]}

Current Phase:
{progress["phase"]}

Current Step:
{progress["current_step"]}

Completed:
{", ".join(progress["completed"])}

Current Task:
{progress["current_task"]}

Next Task:
{progress["next_task"]}
"""

(ROOT / "MENTOR_CONTEXT.md").write_text(
    mentor_context,
    encoding="utf-8"
)


# ---------------------------------
# Update requirements.txt
# ---------------------------------

dependencies = state.get("dependencies", {})

if dependencies.get("update_requirements"):

    new_dependencies = dependencies.get("installed", [])

    requirements_file = ROOT / "requirements.txt"

    if requirements_file.exists():

        try:
            existing = requirements_file.read_text(
                encoding="utf-8"
            ).splitlines()

        except UnicodeDecodeError:

            existing = requirements_file.read_text(
                encoding="utf-16"
            ).splitlines()

    else:
        existing = []


    updated = existing.copy()

    for package in new_dependencies:
        if package not in updated:
            updated.append(package)


    requirements_file.write_text(
        "\n".join(updated) + "\n",
        encoding="utf-8"
    )


# ---------------------------------
# Update CHANGELOG.md
# ---------------------------------

if state.get("changelog", {}).get("enabled"):

    changelog_file = ROOT / "CHANGELOG.md"

    version = project["version"]
    today = datetime.now().strftime("%d-%b-%Y")

    if changelog_file.exists():

        changelog = changelog_file.read_text(
            encoding="utf-8"
        )

    else:
        changelog = "# Changelog\n\n"


    version_header = f"## Version {version} - {today}"

    if version_header not in changelog:

        new_entry = f"""
---

## Version {version} - {today}

### Added

"""

        for item in progress["completed"]:
            new_entry += f"- {item}\n"


        new_entry += f"""
### Current Task

{progress["current_task"]}

### Next Task

{progress["next_task"]}
"""


        changelog += new_entry


        changelog_file.write_text(
            changelog,
            encoding="utf-8"
        )


print("✅ Documentation updated successfully.")