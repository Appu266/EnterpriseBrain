import requests

from app.llm.base_llm import BaseLLM
from config.settings import settings


class OllamaLLM(BaseLLM):

    def __init__(self):

        self.model_name = settings.OLLAMA_MODEL
        self.base_url = settings.OLLAMA_BASE_URL

    def generate(
        self,
        prompt: str
    ) -> str:

        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "keep_alive": "30m",
                "options": {
                    "temperature": 0.2,
                    "num_predict": 250
                }
            },
            timeout=300
        )

        response.raise_for_status()

        result = response.json()

        return result["response"]