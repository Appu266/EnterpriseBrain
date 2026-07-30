import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from app.database import SessionLocal
from app.embeddings.embedding_generator import EmbeddingGenerator
from app.repositories.document_chunk_repository import DocumentChunkRepository
from app.services.retrieval_service import RetrievalService
from app.services.context_builder_service import ContextBuilderService
from app.services.qa_service import QAService
from app.llm.base_llm import BaseLLM


class MockLLM(BaseLLM):

    def generate(
        self,
        prompt: str
    ) -> str:

        return prompt


def main():

    db = SessionLocal()

    try:
        repository = DocumentChunkRepository(db)

        embedding_generator = EmbeddingGenerator()

        context_builder = ContextBuilderService()

        retrieval_service = RetrievalService(
            repository,
            embedding_generator,
            context_builder
        )

        llm = MockLLM()

        qa_service = QAService(
            retrieval_service,
            llm
        )

        question = input(
            "Enter your question: "
        )

        answer = qa_service.answer(
            question
        )

        print("\nResponse:\n")
        print(answer)

    finally:
        db.close()


if __name__ == "__main__":
    main()