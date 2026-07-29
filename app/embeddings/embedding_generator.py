from sentence_transformers import SentenceTransformer


class EmbeddingGenerator:

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2"
    ):

        self.model = SentenceTransformer(
            model_name
        )

    def generate(
        self,
        texts: list[str]
    ) -> list[list[float]]:

        embeddings = self.model.encode(
            texts
        )

        return embeddings.tolist()