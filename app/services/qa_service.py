from dataclasses import dataclass

from app.llm.base_llm import BaseLLM
from app.services.retrieval_service import RetrievalService


@dataclass(frozen=True)
class QAResult:
    context: str
    answer: str


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

        result = self.answer_with_context(
            question
        )

        return result.answer

    def answer_with_context(
        self,
        question: str
    ) -> QAResult:

        context = self.retrieval_service.retrieve(
            question=question,
            limit=3
        )

        prompt = (
            "You are an Oracle PL/SQL code analysis assistant.\n"
            "Answer only from the supplied PL/SQL context.\n"
            "Do not guess or add information not present in the context.\n"
            "Examine the complete supplied context before answering.\n"
            "Do not stop after finding the first few matching items.\n"
            "Return every matching item found across all context sections.\n"
            "Do not repeat the same item.\n"
            "Correctly distinguish tables, sequences, cursors, record types, "
            "collection types, constants, variables, procedures and functions.\n"
            "When asked for tables, identify names appearing after FROM, JOIN, "
            "INSERT INTO, UPDATE, DELETE FROM or MERGE INTO.\n"
            "For a table question, return only the unique table names as a "
            "bullet list. Do not include descriptions, columns, sequences, "
            "PL/SQL types or variables.\n"
            "Keep all other answers concise and complete.\n"
            "If the context does not contain enough information, "
            "say that clearly.\n\n"
            f"Context:\n{context}\n\n"
            f"Question:\n{question}\n\n"
            "Answer:"
        )

        answer = self.llm.generate(
            prompt
        )

        return QAResult(
            context=context,
            answer=answer
        )