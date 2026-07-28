from pathlib import Path


def update_requirements(state: dict, root: Path) -> None:
    """
    Update requirements.txt from project_state.yaml
    """

    dependencies = state["dependencies"]["installed"]

    content = "\n".join(dependencies)

    content += "\n"

    (root / "requirements.txt").write_text(
        content,
        encoding="utf-8",
    )