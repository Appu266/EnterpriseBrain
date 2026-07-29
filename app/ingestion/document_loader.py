from app.validators.file_validator import FileValidator
from app.extractors.metadata_extractor import MetadataExtractor
from app.readers.base_reader import BaseReader
from app.chunkers.text_chunker import TextChunker


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
    ) -> dict:

        # Validate file
        self.validator.validate(file_path)

        # Read file content
        content = self.reader.read(file_path)

        # Extract metadata
        metadata = self.metadata_extractor.extract(file_path)

        # Generate chunks
        chunks = self.chunker.chunk(content)

        metadata["content"] = content
        metadata["chunks"] = chunks

        return metadata