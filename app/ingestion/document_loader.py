from app.validators.file_validator import FileValidator
from app.extractors.metadata_extractor import MetadataExtractor


class DocumentLoader:

    def __init__(self):

        self.validator = FileValidator()
        self.metadata_extractor = MetadataExtractor()

    def load(
        self,
        file_path: str
    ) -> dict:

        # Validate the file
        self.validator.validate(file_path)

        # Extract metadata
        metadata = self.metadata_extractor.extract(file_path)

        return metadata