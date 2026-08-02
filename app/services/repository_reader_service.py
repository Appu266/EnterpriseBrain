from app.factories.reader_factory import ReaderFactory
from app.models.processing_document import ProcessingDocument
from app.models.repository_source_file import (
    RepositorySourceFile
)


class RepositoryReaderService:
    """
    Reads discovered repository source files using ReaderFactory.

    Repository discovery and file reading remain separate concerns.
    """

    def read(
        self,
        source_file: RepositorySourceFile
    ) -> ProcessingDocument:

        reader = ReaderFactory.create(
            source_file.absolute_path
        )

        processing_document = reader.read(
            source_file.absolute_path
        )

        processing_document.metadata.update({
            "repository_name": source_file.repository_name,
            "repository_root": source_file.repository_root,
            "relative_path": source_file.relative_path,
            "extension": source_file.extension,
            "source_type": source_file.source_type,
            **source_file.metadata,
        })

        return processing_document

    def read_all(
        self,
        source_files: list[RepositorySourceFile]
    ) -> list[ProcessingDocument]:

        documents = []

        for source_file in source_files:
            documents.append(
                self.read(
                    source_file
                )
            )

        return documents