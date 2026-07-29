from app.ingestion.document_loader import DocumentLoader
from app.readers.txt_reader import TXTReader
from app.chunkers.text_chunker import TextChunker


reader = TXTReader()

chunker = TextChunker(
    chunk_size=50
)

loader = DocumentLoader(
    reader,
    chunker
)

metadata = loader.load(
    "data/documents/company_policy.txt"
)


print("\nDocument Metadata\n")

for key, value in metadata.items():

    print(f"{key}: {value}")


print("\nGenerated Chunks\n")

for index, chunk in enumerate(metadata["chunks"]):

    print(f"Chunk {index + 1}:")
    print(chunk)
    print("-" * 50)