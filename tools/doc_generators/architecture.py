from pathlib import Path

from doc_generators.constants import PROJECT_MANIFEST_DIR


def _bullet(items: list) -> str:
    return "\n".join(f"- {item}" for item in items)


def generate_architecture(state: dict, root: Path) -> None:
    """
    Generate ARCHITECTURE.md
    """

    architecture = state["application_architecture"]

    modules = architecture["modules"]

    content = f"""# EnterpriseBrain Architecture

---

# Architecture Style

{_bullet(architecture["architecture_style"])}

---

# Layers

{_bullet(architecture["layers"])}

---

# Current Pipeline

{_bullet(architecture["current_pipeline"])}

---

# Upcoming Pipeline

{_bullet(architecture["upcoming_pipeline"])}

---

# Modules

## Configuration

{_bullet(modules["configuration"])}

## Database

{_bullet(modules["database"])}

## Repository

{_bullet(modules["repository"])}

## Service

{_bullet(modules["service"])}

## Ingestion

{_bullet(modules["ingestion"])}

## Readers

{_bullet(modules["readers"])}

## Chunkers

{_bullet(modules["chunkers"])}

## Embeddings

{_bullet(modules["embeddings"])}

## Vector Store

{_bullet(modules["vector_store"])}

---

Last Updated: {state["last_updated"]}
"""

    (PROJECT_MANIFEST_DIR / "ARCHITECTURE.md").write_text(
        content,
        encoding="utf-8",
    )