class DocumentChunker:

    def __init__(
        self,
        chunk_size: int = 500
    ):

        self.chunk_size = chunk_size


    def chunk(
        self,
        text: str
    ) -> list[dict]:

        chunks = []

        words = text.split()

        for index in range(0, len(words), self.chunk_size):

            chunk_words = words[
                index:index + self.chunk_size
            ]

            chunks.append(
                {
                    "chunk_number": len(chunks) + 1,
                    "content": " ".join(chunk_words)
                }
            )

        return chunks