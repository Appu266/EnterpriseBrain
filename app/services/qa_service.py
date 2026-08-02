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
        question: str,
        conversation_history: list[dict[str, str]] | None = None
    ) -> str:

        result = self.answer_with_context(
            question=question,
            conversation_history=conversation_history
        )

        return result.answer

    def answer_with_context(
        self,
        question: str,
        conversation_history: list[dict[str, str]] | None = None
    ) -> QAResult:

        history = conversation_history or []

        retrieval_query = self._build_retrieval_query(
            question=question,
            conversation_history=history
        )

        context = self.retrieval_service.retrieve(
            question=retrieval_query,
            limit=3
        )

        formatted_history = self._format_conversation_history(
            history
        )

        prompt = (
            "You are an enterprise document analysis assistant.\n"
            "Answer only from the supplied document context.\n"
            "Use the conversation history to understand references "
            "such as 'it', 'them', 'those', 'that item' or "
            "'the previous answer'.\n"
            "When the user asks to list something mentioned previously, "
            "return the actual item names rather than repeating only "
            "the previous count.\n"
            "Do not treat conversation history as a factual source when "
            "it conflicts with the document context.\n"
            "Do not guess or add information not present in the context.\n"
            "Examine the complete supplied context before answering.\n"
            "Do not repeat the same item.\n"
            "Keep the answer concise and complete.\n"
            "If the context does not contain enough information, "
            "say that clearly.\n\n"
            f"Conversation History:\n{formatted_history}\n\n"
            f"Document Context:\n{context}\n\n"
            f"Current Question:\n{question}\n\n"
            "Answer:"
        )

        answer = self.llm.generate(
            prompt
        )

        return QAResult(
            context=context,
            answer=answer
        )

    @staticmethod
    def _build_retrieval_query(
        question: str,
        conversation_history: list[dict[str, str]]
    ) -> str:

        if not conversation_history:
            return question

        recent_messages = conversation_history[-4:]

        relevant_parts = []

        for message in recent_messages:
            content = message.get(
                "content",
                ""
            ).strip()

            if content:
                relevant_parts.append(
                    content
                )

        relevant_parts.append(
            question
        )

        return "\n".join(
            relevant_parts
        )

    @staticmethod
    def _format_conversation_history(
        conversation_history: list[dict[str, str]]
    ) -> str:

        if not conversation_history:
            return "No previous conversation."

        recent_messages = conversation_history[-6:]

        formatted_messages = []

        for message in recent_messages:
            role = message.get(
                "role",
                "user"
            ).strip().lower()

            content = message.get(
                "content",
                ""
            ).strip()

            if not content:
                continue

            display_role = (
                "Assistant"
                if role == "assistant"
                else "User"
            )

            formatted_messages.append(
                f"{display_role}: {content}"
            )

        if not formatted_messages:
            return "No previous conversation."

        return "\n".join(
            formatted_messages
        )