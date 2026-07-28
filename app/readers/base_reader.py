from abc import ABC, abstractmethod


class BaseReader(ABC):
    """
    Base contract for all document readers.

    Every reader implementation must provide
    a method to extract text content from a file.
    """

    @abstractmethod
    def read(
        self,
        file_path: str
    ) -> str:
        """
        Read document content.

        Args:
            file_path: Path of the document

        Returns:
            Extracted text content
        """

        pass