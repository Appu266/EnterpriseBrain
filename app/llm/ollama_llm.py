from app.llm.base_llm import BaseLLM


class OllamaLLM(BaseLLM):

    def __init__(
        self,
        model_name: str = "llama3"
    ):
        self.model_name = model_name


    def generate(
        self,
        prompt: str
    ) -> str:

        raise NotImplementedError(
            "Ollama integration not implemented yet."
        )