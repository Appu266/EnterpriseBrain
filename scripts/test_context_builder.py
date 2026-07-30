import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from app.services.context_builder_service import ContextBuilderService


class MockChunk:
    def __init__(self, content):
        self.content = content


def main():

    chunks = [
        (
            MockChunk("Customer validation package details"),
            0.12
        ),
        (
            MockChunk("Procedure checks customer status"),
            0.18
        )
    ]

    service = ContextBuilderService()

    context = service.build_context(chunks)

    print(context)


if __name__ == "__main__":
    main()