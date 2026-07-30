import requests

from app.llm.base_llm import BaseLLM


class OllamaLLM(BaseLLM):

    def __init__(
        self,
        model_name: str = "llama3",
        base_url: str = "http://localhost:11434"
    ):
        self.model_name = model_name
        self.base_url = base_url


    def generate(
        self,
        prompt: str
    ) -> str:

        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model_name,
                "prompt": prompt,
                "stream": False
            }
        )

        response.raise_for_status()

        result = response.json()

        return result["response"]