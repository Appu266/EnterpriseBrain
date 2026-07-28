from pathlib import Path


class FileValidator:

    SUPPORTED_EXTENSIONS = {
        ".pdf",
        ".docx",
        ".txt"
    }

    def exists(
        self,
        file_path: str
    ) -> bool:

        return Path(file_path).exists()

    def validate_extension(
        self,
        file_path: str
    ) -> bool:

        extension = Path(file_path).suffix.lower()

        return extension in self.SUPPORTED_EXTENSIONS

    def validate(
        self,
        file_path: str
    ) -> None:

        if not self.exists(file_path):
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        if not self.validate_extension(file_path):
            raise ValueError(
                f"Unsupported file type: {Path(file_path).suffix}"
            )