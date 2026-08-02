import tempfile
from pathlib import Path

import streamlit as st

from app.database import SessionLocal
from app.embeddings.embedding_generator import EmbeddingGenerator
from app.llm.ollama_llm import OllamaLLM
from app.readers.txt_reader import TXTReader
from app.services.document_assistant_service import (
    DocumentAssistantService
)


SUPPORTED_FILE_TYPES = [
    "txt",
    "sql",
    "pls",
    "pks",
    "pkb"
]


def initialize_session_state() -> None:
    if "assistant_service" not in st.session_state:
        st.session_state.assistant_service = None

    if "database_session" not in st.session_state:
        st.session_state.database_session = None

    if "active_document_name" not in st.session_state:
        st.session_state.active_document_name = None

    if "uploaded_file_signature" not in st.session_state:
        st.session_state.uploaded_file_signature = None

    if "messages" not in st.session_state:
        st.session_state.messages = []


def create_assistant_service() -> DocumentAssistantService:
    database_session = SessionLocal()

    assistant_service = DocumentAssistantService(
        db=database_session,
        reader=TXTReader(),
        llm=OllamaLLM(),
        embedding_generator=EmbeddingGenerator()
    )

    st.session_state.database_session = database_session
    st.session_state.assistant_service = assistant_service

    return assistant_service


def close_existing_service() -> None:
    assistant_service = st.session_state.assistant_service

    if assistant_service is not None:
        assistant_service.close_document()

    database_session = st.session_state.database_session

    if database_session is not None:
        database_session.close()

    st.session_state.assistant_service = None
    st.session_state.database_session = None


def save_uploaded_file(
    uploaded_file
) -> Path:
    file_suffix = Path(
        uploaded_file.name
    ).suffix

    with tempfile.NamedTemporaryFile(
        mode="wb",
        suffix=file_suffix,
        delete=False
    ) as temporary_file:
        temporary_file.write(
            uploaded_file.getbuffer()
        )

        return Path(
            temporary_file.name
        )


def ingest_uploaded_document(
    uploaded_file
) -> None:
    temporary_path = save_uploaded_file(
        uploaded_file
    )

    try:
        close_existing_service()

        assistant_service = create_assistant_service()

        assistant_service.ingest_document(
            temporary_path
        )

        st.session_state.active_document_name = (
            uploaded_file.name
        )

        st.session_state.uploaded_file_signature = (
            uploaded_file.name,
            uploaded_file.size
        )

        st.session_state.messages = []

    finally:
        temporary_path.unlink(
            missing_ok=True
        )


def render_chat_history() -> None:
    for message in st.session_state.messages:
        with st.chat_message(
            message["role"]
        ):
            st.markdown(
                message["content"]
            )


def main() -> None:
    st.set_page_config(
        page_title="EnterpriseBrain",
        page_icon="🧠",
        layout="centered"
    )

    initialize_session_state()

    st.title("EnterpriseBrain")
    st.caption(
        "Upload a document and ask questions about its contents."
    )

    uploaded_file = st.file_uploader(
        "Upload document",
        type=SUPPORTED_FILE_TYPES,
        accept_multiple_files=False
    )

    if uploaded_file is not None:
        uploaded_signature = (
            uploaded_file.name,
            uploaded_file.size
        )

        if (
            uploaded_signature
            != st.session_state.uploaded_file_signature
        ):
            with st.spinner(
                "Preparing document..."
            ):
                try:
                    ingest_uploaded_document(
                        uploaded_file
                    )

                except Exception as error:
                    close_existing_service()

                    st.error(
                        "The document could not be processed."
                    )

                    st.exception(
                        error
                    )

                    return

    active_document_name = (
        st.session_state.active_document_name
    )

    if active_document_name is None:
        st.info(
            "Upload a supported document to begin."
        )
        return

    st.success(
        f"Active document: {active_document_name}"
    )

    render_chat_history()

    question = st.chat_input(
        "Ask a question about the document"
    )

    if not question:
        return

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(
            question
        )

    assistant_service = (
        st.session_state.assistant_service
    )

    with st.chat_message("assistant"):
        with st.spinner(
            "Thinking..."
        ):
            try:
                conversation_history = (
                    st.session_state.messages[:-1]
                )

                result = assistant_service.ask(
                    question=question,
                    conversation_history=conversation_history
                )

                st.markdown(
                    result.answer
                )

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result.answer
                })

            except Exception as error:
                error_message = (
                    "EnterpriseBrain could not answer "
                    "the question."
                )

                st.error(
                    error_message
                )

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_message
                })


if __name__ == "__main__":
    main()