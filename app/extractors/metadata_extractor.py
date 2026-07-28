from pathlib import Path
from datetime import datetime


class MetadataExtractor:

    FILE_TYPES = {
        ".pdf": "PDF",
        ".docx": "DOCX",
        ".txt": "TXT"
    }

    def extract(
        self,
        file_path: str
    ) -> dict:

        path = Path(file_path)

        stats = path.stat()

        extension = path.suffix.lower()

        return {
            "filename": path.name,
            "file_type": self.FILE_TYPES.get(extension, "UNKNOWN"),
            "file_path": str(path),
            "file_size": stats.st_size,
            "created_at": datetime.fromtimestamp(stats.st_ctime),
            "modified_at": datetime.fromtimestamp(stats.st_mtime)
        }