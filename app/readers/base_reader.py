from abc import ABC, abstractmethod

from app.models.processing_document import ProcessingDocument


class BaseReader(ABC):
    """
    Base contract for all document readers.

    Every reader implementation must provide
    a method to extract document content from a file.
    """

    @abstractmethod
    def read(
        self,
        file_path: str
    ) -> ProcessingDocument:
        """
        Read document content.

        Args:
            file_path: Path of the document

        Returns:
            ProcessingDocument object
        """

        pass