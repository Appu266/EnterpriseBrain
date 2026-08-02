import os

os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from huggingface_hub import logging as hf_logging
from sentence_transformers import SentenceTransformer
from transformers.utils import logging as transformers_logging


hf_logging.set_verbosity_error()
transformers_logging.set_verbosity_error()
transformers_logging.disable_progress_bar()


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
            texts,
            show_progress_bar=False
        )

        return embeddings.tolist()