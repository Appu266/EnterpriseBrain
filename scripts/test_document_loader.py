from app.chunkers.text_chunker import TextChunker
from app.ingestion.document_loader import DocumentLoader
from app.readers.txt_reader import TXTReader


reader = TXTReader()

chunker = TextChunker(
    chunk_size=50
)

loader = DocumentLoader(
    reader,
    chunker
)

document = loader.load(
    "data/documents/company_policy.txt"
)


print("\nProcessing Document\n")

print(f"File Name: {document.file_name}")
print(f"File Path: {document.file_path}")
print(f"Content: {document.content}")


print("\nDocument Metadata\n")

for key, value in document.metadata.items():

    print(f"{key}: {value}")


print("\nGenerated Chunks\n")

for index, chunk in enumerate(document.chunks):

    print(f"Chunk {index + 1}:")
    print(chunk)
    print("-" * 50)