from app.services.repository_discovery_service import (
    RepositoryDiscoveryService
)
from app.services.repository_reader_service import (
    RepositoryReaderService
)


def main() -> None:
    repository_path = input(
        "Enter the repository path: "
    ).strip()

    if not repository_path:
        print("Repository path cannot be empty.")
        return

    discovery_service = RepositoryDiscoveryService()
    reader_service = RepositoryReaderService()

    source_files = discovery_service.discover(
        repository_path
    )

    print()
    print(
        f"Discovered source files: {len(source_files)}"
    )

    if not source_files:
        print(
            "No supported repository source files were found."
        )
        return

    documents = reader_service.read_all(
        source_files
    )

    print(
        f"Read documents: {len(documents)}"
    )
    print()

    for index, document in enumerate(
        documents,
        start=1
    ):
        print(
            f"{index}. {document.metadata['relative_path']}"
        )
        print(
            f"   File name: {document.file_name}"
        )
        print(
            f"   Extension: {document.metadata['extension']}"
        )
        print(
            f"   Source type: {document.metadata['source_type']}"
        )
        print(
            f"   Content length: {len(document.content)} characters"
        )
        print()

    if len(documents) != len(source_files):
        raise AssertionError(
            "Not all discovered source files were read."
        )

    if any(
        not document.content.strip()
        for document in documents
    ):
        raise AssertionError(
            "One or more documents have empty content."
        )

    print(
        "Repository reader test completed successfully."
    )


if __name__ == "__main__":
    main()