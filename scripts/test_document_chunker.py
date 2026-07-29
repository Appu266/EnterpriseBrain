from app.chunkers.document_chunker import DocumentChunker


def test_document_chunker():

    text = """
    EnterpriseBrain is an AI-powered Enterprise Knowledge Assistant.
    It understands enterprise documents and helps users find
    information from large knowledge repositories.
    """

    chunker = DocumentChunker(
        chunk_size=10
    )

    chunks = chunker.chunk(text)

    print("\nChunk Results\n")

    for chunk in chunks:
        print(f"Chunk Number: {chunk['chunk_number']}")
        print(f"Content: {chunk['content']}")
        print("-" * 50)


if __name__ == "__main__":
    test_document_chunker()