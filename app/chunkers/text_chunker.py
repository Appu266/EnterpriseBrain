from typing import List


class TextChunker:

    def __init__(
        self,
        chunk_size: int = 500
    ):
        self.chunk_size = chunk_size

    def chunk(
        self,
        text: str
    ) -> List[str]:

        chunks = []

        start = 0

        while start < len(text):

            end = start + self.chunk_size

            chunks.append(
                text[start:end]
            )

            start = end

        return chunks