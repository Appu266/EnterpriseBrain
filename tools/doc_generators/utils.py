from pathlib import Path
import yaml


def load_project_state(root: Path) -> dict:
    """
    Load project_state.yaml
    """

    yaml_file = root / "project_state.yaml"

    with open(yaml_file, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)