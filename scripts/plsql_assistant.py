from pathlib import Path


def run_assistant() -> None:
    print("\nEnterpriseBrain - PL/SQL Assistant\n")

    file_path = input(
        "Enter the PL/SQL document path: "
    ).strip()

    if not file_path:
        print("\nDocument path cannot be empty.")
        return

    print("\nLoading EnterpriseBrain components...")

    from app.chunkers.document_chunker import DocumentChunker
    from app.chunkers.text_chunker import TextChunker
    from app.database import SessionLocal
    from app.embeddings.embedding_generator import EmbeddingGenerator
    from app.ingestion.document_loader import DocumentLoader
    from app.llm.ollama_llm import OllamaLLM
    from app.readers.txt_reader import TXTReader
    from app.repositories.document_chunk_repository import (
        DocumentChunkRepository
    )
    from app.services.chunk_service import ChunkService
    from app.services.context_builder_service import (
        ContextBuilderService
    )
    from app.services.document_service import DocumentService
    from app.services.qa_service import QAService
    from app.services.retrieval_service import RetrievalService

    db = SessionLocal()

    try:
        reader = TXTReader()

        text_chunker = TextChunker(
            chunk_size=1000
        )

        document_loader = DocumentLoader(
            reader=reader,
            chunker=text_chunker
        )

        processing_document = document_loader.load(
            file_path
        )

        document_service = DocumentService()

        stored_document = document_service.create_document(
            db=db,
            filename=processing_document.file_name,
            file_type=processing_document.metadata["file_type"],
            file_path=processing_document.file_path
        )

        document_chunker = DocumentChunker(
            chunk_size=500
        )

        chunk_repository = DocumentChunkRepository(
            db
        )

        print("Loading embedding model...")

        embedding_generator = EmbeddingGenerator()

        chunk_service = ChunkService(
            chunker=document_chunker,
            repository=chunk_repository,
            embedding_generator=embedding_generator
        )

        print("Generating and storing document embeddings...")

        stored_chunks = chunk_service.create_and_store_chunks(
            document_id=stored_document.id,
            document_text=processing_document.content
        )

        context_builder = ContextBuilderService()

        retrieval_service = RetrievalService(
            repository=chunk_repository,
            embedding_generator=embedding_generator,
            context_builder=context_builder,
            document_id=stored_document.id
        )

        llm = OllamaLLM()

        qa_service = QAService(
            retrieval_service=retrieval_service,
            llm=llm
        )

        print("\nDocument ingested successfully.")
        print(
            f"File: {processing_document.file_name}"
        )
        print(
            f"Stored chunks: {len(stored_chunks)}"
        )

        print(
            "\nAsk questions about the PL/SQL package."
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

            answer = qa_service.answer(
                question
            )

            print("\nAnswer:\n")
            print(answer)
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

    except Exception as error:
        print(
            "\nUnexpected assistant error:"
        )
        print(
            f"{type(error).__name__}: {error!r}"
        )


if __name__ == "__main__":
    main()