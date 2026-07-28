from pathlib import Path

from doc_generators.utils import load_project_state
from doc_generators.vision import generate_project_vision
from doc_generators.status import generate_project_status
from doc_generators.mentor import generate_mentor_context
from doc_generators.architecture import generate_architecture
from doc_generators.changelog import generate_changelog
from doc_generators.requirements import update_requirements


ROOT = Path(__file__).resolve().parents[1]


def main():
    """
    EnterpriseBrain Documentation Generator

    Reads project_state.yaml and regenerates all project
    documentation from a single source of truth.
    """

    print("=" * 60)
    print("EnterpriseBrain Documentation Generator")
    print("=" * 60)
    print()

    state = load_project_state(ROOT)

    generators = [
        ("PROJECT_VISION.md", generate_project_vision),
        ("PROJECT_STATUS.md", generate_project_status),
        ("MENTOR_CONTEXT.md", generate_mentor_context),
        ("ARCHITECTURE.md", generate_architecture),
        ("CHANGELOG.md", generate_changelog),
    ]

    for document_name, generator in generators:
        print(f"Generating {document_name}...")
        generator(state, ROOT)

    if state["dependencies"]["update_requirements"]:
        print("Updating requirements.txt...")
        update_requirements(state, ROOT)

    print()
    print("=" * 60)
    print("Documentation generated successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()