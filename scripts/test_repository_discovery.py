from pathlib import Path

from app.services.repository_discovery_service import (
    RepositoryDiscoveryService
)


def main() -> None:
    repository_path = input(
        "Enter the repository path: "
    ).strip()

    if not repository_path:
        print("Repository path cannot be empty.")
        return

    discovery_service = RepositoryDiscoveryService()

    discovered_files = discovery_service.discover(
        repository_path
    )

    print()
    print(
        f"Repository: {Path(repository_path).resolve().name}"
    )
    print(
        f"Discovered database source files: "
        f"{len(discovered_files)}"
    )
    print()

    if not discovered_files:
        print(
            "No supported database source files were found."
        )
        return

    for index, source_file in enumerate(
        discovered_files,
        start=1
    ):
        print(
            f"{index}. {source_file.relative_path}"
        )
        print(
            f"   Extension: {source_file.extension}"
        )
        print(
            f"   Size: "
            f"{source_file.metadata['size_bytes']} bytes"
        )
        print(
            f"   Source type: {source_file.source_type}"
        )
        print()


if __name__ == "__main__":
    main()