from pathlib import Path


def generate_changelog(state: dict, root: Path) -> None:
    """
    Generate CHANGELOG.md
    """

    progress = state["progress"]

    content = f"""# EnterpriseBrain Changelog

## Version

{state["project"]["version"]}

---

## Completed Milestones

"""

    for milestone in progress["completed"]:
        content += f"- {milestone}\n"

    content += f"""

---

Last Updated: {state["last_updated"]}
"""

    (root / "CHANGELOG.md").write_text(
        content,
        encoding="utf-8",
    )