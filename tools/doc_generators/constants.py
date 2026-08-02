from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

PROJECT_MANIFEST_DIR = (
    ROOT / "project_manifest"
)

PROJECT_STATE_FILE = (
    PROJECT_MANIFEST_DIR / "project_state.yaml"
)

REQUIREMENTS_FILE = (
    ROOT / "requirements.txt"
)