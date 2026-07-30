from app.services.retrieval_service import RetrievalService
from app.llm.base_llm import BaseLLM


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
            question
        )

        prompt = (
            "Use the following enterprise context "
            "to answer the question.\n\n"
            f"Context:\n{context}\n\n"
            f"Question:\n{question}"
        )

        return self.llm.generate(
            prompt
        )