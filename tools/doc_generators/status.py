from pathlib import Path


def generate_project_status(state: dict, root: Path) -> None:
    """
    Generate PROJECT_STATUS.md
    """

    progress = state["progress"]

    completed = "\n".join(
        f"- [x] {item}"
        for item in progress["completed"]
    )

    content = f"""# EnterpriseBrain - Project Status

## Current Phase

{progress["phase"]}

---

## Current Step

{progress["current_step"]}

---

## Completed Milestones

{completed}

---

## Current Task

{progress["current_task"]}

---

## Next Task

{progress["next_task"]}

---

Last Updated: {state["last_updated"]}
"""

    (root / "PROJECT_STATUS.md").write_text(
        content,
        encoding="utf-8",
    )