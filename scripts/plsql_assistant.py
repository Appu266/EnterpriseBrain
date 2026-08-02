from pathlib import Path

from app.presentation.cli import CLI
from config.settings import settings


def run_assistant() -> None:
    CLI.title("EnterpriseBrain - Document Assistant")

    file_path = input(
        "Enter the document path: "
    ).strip()

    if not file_path:
        print("\nDocument path cannot be empty.")
        return

    if settings.is_debug:
        print("\nLoading EnterpriseBrain components...")

    from app.database import SessionLocal
    from app.embeddings.embedding_generator import EmbeddingGenerator
    from app.llm.ollama_llm import OllamaLLM
    from app.readers.txt_reader import TXTReader
    from app.services.document_assistant_service import (
        DocumentAssistantService
    )

    db = SessionLocal()

    try:
        assistant_service = DocumentAssistantService(
            db=db,
            reader=TXTReader(),
            llm=OllamaLLM(),
            embedding_generator=EmbeddingGenerator()
        )

        ingestion_result = assistant_service.ingest_document(
            file_path
        )

        if settings.is_debug:
            print("\nDocument ingested successfully.")
            print(
                f"File: {ingestion_result.file_name}"
            )
            print(
                f"Stored chunks: "
                f"{ingestion_result.stored_chunk_count}"
            )

        print(
            "\nAsk questions about the document."
        )
        print(
            "Type 'exit' or press Ctrl+C to close the assistant.\n"
        )

        while True:
            question = input(
                "Question: "
            ).strip()

            if question.lower() == "exit":
                print(
                    "\nEnterpriseBrain assistant closed."
                )
                return

            if not question:
                print(
                    "Please enter a question or type 'exit'.\n"
                )
                continue

            result = assistant_service.answer_question(
                question
            )

            if settings.is_debug:
                print("\nRetrieved Context:\n")
                print("-" * 70)

                if result.context:
                    print(result.context)
                else:
                    print(
                        "No relevant document context was retrieved."
                    )

                print("-" * 70)

            print("\nAnswer:\n")
            print(result.answer)
            print()

    finally:
        db.close()


def main() -> None:
    try:
        run_assistant()

    except KeyboardInterrupt:
        print(
            "\n\nEnterpriseBrain assistant closed."
        )

    except FileNotFoundError as error:
        print(
            f"\nFile not found: {Path(error.filename or '')}"
        )

    except ValueError as error:
        print(
            f"\nValidation error: {error}"
        )

    except RuntimeError as error:
        print(
            f"\nAssistant error: {error}"
        )

    except Exception as error:
        print(
            "\nUnexpected assistant error:"
        )
        print(
            f"{type(error).__name__}: {error!r}"
        )


if __name__ == "__main__":
    main()