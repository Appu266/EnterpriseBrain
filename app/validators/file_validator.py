from pathlib import Path


class FileValidator:

    SUPPORTED_EXTENSIONS = {
        ".txt",
        ".sql",
        ".pls",
        ".pks",
        ".pkb",
    }

    def exists(
        self,
        file_path: str,
    ) -> bool:

        return Path(file_path).is_file()

    def validate_extension(
        self,
        file_path: str,
    ) -> bool:

        extension = Path(file_path).suffix.lower()

        return extension in self.SUPPORTED_EXTENSIONS

    def validate(
        self,
        file_path: str,
    ) -> None:

        if not self.exists(file_path):
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        if not self.validate_extension(file_path):
            supported_extensions = ", ".join(
                sorted(self.SUPPORTED_EXTENSIONS)
            )

            raise ValueError(
                f"Unsupported file type: "
                f"{Path(file_path).suffix or '[no extension]'}. "
                f"Supported file types: {supported_extensions}"
            )