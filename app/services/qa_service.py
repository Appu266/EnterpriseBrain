from app.llm.base_llm import BaseLLM
from app.services.retrieval_service import RetrievalService


class QAService:

    def __init__(
        self,
        retrieval_service: RetrievalService,
        llm: BaseLLM
    ):
        self.retrieval_service = retrieval_service
        self.llm = llm

    def answer(
        self,
        question: str
    ) -> str:

        context = self.retrieval_service.retrieve(
            question=question,
            limit=3
        )

        prompt = (
            "You are an Oracle PL/SQL assistant.\n"
            "Answer only from the supplied package context.\n"
            "Be accurate and concise.\n"
            "If the context does not contain enough information, "
            "say that clearly.\n\n"
            f"Context:\n{context}\n\n"
            f"Question:\n{question}\n\n"
            "Answer:"
        )

        return self.llm.generate(
            prompt
        )