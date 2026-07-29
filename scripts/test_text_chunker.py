from pathlib import Path

from app.chunkers.text_chunker import TextChunker


file_path = Path(
    "data/documents/company_policy.txt"
)

text = file_path.read_text(
    encoding="utf-8"
)


chunker = TextChunker(
    chunk_size=50
)

chunks = chunker.chunk(text)


print("\nGenerated Chunks\n")

for index, chunk in enumerate(chunks):
    print(f"Chunk {index + 1}:")
    print(chunk)
    print("-" * 50)