from app.chunkers.text_chunker import TextChunker
from app.extractors.metadata_extractor import MetadataExtractor
from app.models.processing_document import ProcessingDocument
from app.readers.base_reader import BaseReader
from app.validators.file_validator import FileValidator


class DocumentLoader:

    def __init__(
        self,
        reader: BaseReader,
        chunker: TextChunker
    ):

        self.validator = FileValidator()
        self.metadata_extractor = MetadataExtractor()
        self.reader = reader
        self.chunker = chunker

    def load(
        self,
        file_path: str
    ) -> ProcessingDocument:

        # Validate file
        self.validator.validate(file_path)

        # Read document
        document = self.reader.read(file_path)

        # Extract and attach metadata
        document.metadata = self.metadata_extractor.extract(file_path)

        # Generate and attach chunks
        document.chunks = self.chunker.chunk(document.content)

        return document