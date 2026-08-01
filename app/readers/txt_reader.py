from pathlib import Path

from app.models.processing_document import ProcessingDocument
from app.readers.base_reader import BaseReader


class TXTReader(BaseReader):
    """
    Reader implementation for plain text (.txt) documents.
    """

    def read(
        self,
        file_path: str
    ) -> ProcessingDocument:

        path = Path(file_path)

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            return ProcessingDocument(
                file_name=path.name,
                file_path=str(path),
                content=file.read()
            )