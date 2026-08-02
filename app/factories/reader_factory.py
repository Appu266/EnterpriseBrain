from pathlib import Path

from app.readers.base_reader import BaseReader
from app.readers.txt_reader import TXTReader


class ReaderFactory:
    """
    Creates the appropriate document reader for a source file.

    Readers are selected using the file extension. New reader
    implementations can be registered without changing calling code.
    """

    _reader_registry: dict[str, type[BaseReader]] = {
        ".txt": TXTReader,
        ".sql": TXTReader,
        ".pls": TXTReader,
        ".pks": TXTReader,
        ".pkb": TXTReader,
    }

    @classmethod
    def create(
        cls,
        file_path: str | Path
    ) -> BaseReader:

        extension = Path(
            file_path
        ).suffix.lower()

        reader_class = cls._reader_registry.get(
            extension
        )

        if reader_class is None:
            supported_extensions = ", ".join(
                sorted(cls._reader_registry)
            )

            raise ValueError(
                f"No reader is registered for file type: "
                f"{extension or '[no extension]'}. "
                f"Supported file types: {supported_extensions}"
            )

        return reader_class()

    @classmethod
    def register(
        cls,
        extensions: set[str],
        reader_class: type[BaseReader]
    ) -> None:

        if not issubclass(
            reader_class,
            BaseReader
        ):
            raise TypeError(
                "Registered reader must inherit from BaseReader."
            )

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

            cls._reader_registry[
                normalized_extension
            ] = reader_class

    @classmethod
    def supports(
        cls,
        file_path: str | Path
    ) -> bool:

        extension = Path(
            file_path
        ).suffix.lower()

        return extension in cls._reader_registry

    @classmethod
    def supported_extensions(
        cls
    ) -> set[str]:

        return set(
            cls._reader_registry
        )