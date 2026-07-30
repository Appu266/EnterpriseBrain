class ContextBuilderService:

    def build_context(
        self,
        retrieved_chunks: list
    ) -> str:

        if not retrieved_chunks:
            return ""

        context_parts = []

        for index, item in enumerate(
            retrieved_chunks,
            start=1
        ):
            chunk = item[0]

            context_parts.append(
                f"Document Reference {index}:\n\n"
                f"{chunk.content}"
            )

        return "\n\n---\n\n".join(
            context_parts
        )