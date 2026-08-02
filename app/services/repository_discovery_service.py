from pathlib import Path

from app.models.repository_source_file import (
    RepositorySourceFile
)


class RepositoryDiscoveryService:
    """
    Discovers supported source files inside a local repository.

    The service is generic and configurable. It does not contain
    PL/SQL parsing or source-code analysis logic.
    """

    DEFAULT_SUPPORTED_EXTENSIONS = {
        ".sql",
        ".pls",
        ".pks",
        ".pkb",
    }

    DEFAULT_EXCLUDED_DIRECTORIES = {
        ".git",
        ".idea",
        ".vscode",
        ".venv",
        "node_modules",
        "__pycache__",
        "build",
        "dist",
        "target",
    }

    def __init__(
        self,
        supported_extensions: set[str] | None = None,
        excluded_directories: set[str] | None = None,
        source_type: str = "database"
    ):
        self.supported_extensions = (
            self._normalize_extensions(
                supported_extensions
                or self.DEFAULT_SUPPORTED_EXTENSIONS
            )
        )

        self.excluded_directories = {
            directory.lower()
            for directory in (
                excluded_directories
                or self.DEFAULT_EXCLUDED_DIRECTORIES
            )
        }

        self.source_type = source_type

    def discover(
        self,
        repository_path: str | Path
    ) -> list[RepositorySourceFile]:

        repository_root = Path(
            repository_path
        ).expanduser().resolve()

        self._validate_repository_path(
            repository_root
        )

        repository_name = repository_root.name

        discovered_files = []

        for file_path in repository_root.rglob("*"):
            if not file_path.is_file():
                continue

            if self._is_excluded(
                file_path=file_path,
                repository_root=repository_root
            ):
                continue

            extension = file_path.suffix.lower()

            if extension not in self.supported_extensions:
                continue

            relative_path = file_path.relative_to(
                repository_root
            )

            discovered_files.append(
                RepositorySourceFile(
                    repository_name=repository_name,
                    repository_root=str(repository_root),
                    file_name=file_path.name,
                    relative_path=relative_path.as_posix(),
                    absolute_path=str(file_path),
                    extension=extension,
                    source_type=self.source_type,
                    metadata={
                        "size_bytes": file_path.stat().st_size,
                        "parent_directory": (
                            relative_path.parent.as_posix()
                        ),
                    }
                )
            )

        return sorted(
            discovered_files,
            key=lambda source_file: (
                source_file.relative_path.lower()
            )
        )

    def _is_excluded(
        self,
        file_path: Path,
        repository_root: Path
    ) -> bool:

        relative_parts = file_path.relative_to(
            repository_root
        ).parts[:-1]

        return any(
            part.lower() in self.excluded_directories
            for part in relative_parts
        )

    @staticmethod
    def _normalize_extensions(
        extensions: set[str]
    ) -> set[str]:

        normalized_extensions = set()

        for extension in extensions:
            normalized_extension = (
                extension.strip().lower()
            )

            if not normalized_extension:
                continue

            if not normalized_extension.startswith("."):
                normalized_extension = (
                    f".{normalized_extension}"
                )

            normalized_extensions.add(
                normalized_extension
            )

        return normalized_extensions

    @staticmethod
    def _validate_repository_path(
        repository_root: Path
    ) -> None:

        if not repository_root.exists():
            raise FileNotFoundError(
                f"Repository path not found: "
                f"{repository_root}"
            )

        if not repository_root.is_dir():
            raise ValueError(
                f"Repository path is not a directory: "
                f"{repository_root}"
            )