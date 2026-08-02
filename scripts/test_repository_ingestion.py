def main() -> None:
    repository_path = input(
        "Enter the repository path: "
    ).strip()

    if not repository_path:
        print(
            "Repository path cannot be empty."
        )
        return

    from config.settings import settings

    if settings.is_debug:
        print(
            "\nLoading EnterpriseBrain components..."
        )

    from app.database import SessionLocal
    from app.embeddings.embedding_generator import (
        EmbeddingGenerator
    )
    from app.services.indexing_run_service import (
        IndexingRunService
    )
    from app.services.knowledge_source_service import (
        KnowledgeSourceService
    )
    from app.services.repository_ingestion_service import (
        RepositoryIngestionService
    )

    db = SessionLocal()

    try:
        ingestion_service = RepositoryIngestionService(
            db=db,
            embedding_generator=EmbeddingGenerator()
        )

        result = ingestion_service.ingest(
            repository_path
        )

        print()
        print(
            f"Repository: {result.repository_name}"
        )
        print(
            f"Repository root: {result.repository_root}"
        )
        print(
            f"Discovered files: "
            f"{result.discovered_file_count}"
        )
        print(
            f"Ingested files: "
            f"{result.ingested_file_count}"
        )
        print(
            f"Stored chunks: "
            f"{result.stored_chunk_count}"
        )
        print()

        for index, file_result in enumerate(
            result.files,
            start=1
        ):
            print(
                f"{index}. {file_result.relative_path}"
            )
            print(
                f"   Document ID: "
                f"{file_result.document_id}"
            )
            print(
                f"   File type: "
                f"{file_result.file_type}"
            )
            print(
                f"   Stored chunks: "
                f"{file_result.stored_chunk_count}"
            )
            print()

        print("Repository Context")
        print("-" * 50)
        print(
            f"Repository name: "
            f"{result.context.repository_name}"
        )
        print(
            f"Repository root: "
            f"{result.context.repository_root}"
        )
        print(
            f"Source type: "
            f"{result.context.source.source_type.value}"
        )
        print(
            f"Document count: "
            f"{result.context.document_count}"
        )
        print(
            f"Document IDs: "
            f"{result.context.document_ids}"
        )
        print(
            f"Is empty: "
            f"{result.context.is_empty}"
        )
        print()

        if (
            result.discovered_file_count
            != result.ingested_file_count
        ):
            raise AssertionError(
                "Not all discovered files were ingested."
            )

        if result.stored_chunk_count <= 0:
            raise AssertionError(
                "No repository chunks were stored."
            )

        if result.context.is_empty:
            raise AssertionError(
                "Repository ingestion context is empty."
            )

        if (
            result.context.document_count
            != result.ingested_file_count
        ):
            raise AssertionError(
                "Repository context document count "
                "does not match ingested file count."
            )

        knowledge_source_id = (
            result.context.source.metadata[
                "knowledge_source_id"
            ]
        )

        indexing_run_id = (
            result.context.source.metadata[
                "indexing_run_id"
            ]
        )

        knowledge_source_service = (
            KnowledgeSourceService()
        )

        indexing_run_service = (
            IndexingRunService()
        )

        persistent_source = (
            knowledge_source_service.get_knowledge_source(
                db=db,
                knowledge_source_id=knowledge_source_id
            )
        )

        if persistent_source is None:
            raise AssertionError(
                "Persistent knowledge source was not found."
            )

        if persistent_source.name != result.repository_name:
            raise AssertionError(
                "Persistent knowledge-source name "
                "does not match the repository name."
            )

        if persistent_source.location != result.repository_root:
            raise AssertionError(
                "Persistent knowledge-source location "
                "does not match the repository root."
            )

        indexing_run = (
            indexing_run_service.get_indexing_run(
                db=db,
                indexing_run_id=indexing_run_id
            )
        )

        if indexing_run is None:
            raise AssertionError(
                "Persistent indexing run was not found."
            )

        if indexing_run.status != "completed":
            raise AssertionError(
                "Indexing run was not completed."
            )

        if (
            indexing_run.documents_discovered
            != result.discovered_file_count
        ):
            raise AssertionError(
                "Indexing-run discovered count "
                "does not match the ingestion result."
            )

        if (
            indexing_run.documents_processed
            != result.ingested_file_count
        ):
            raise AssertionError(
                "Indexing-run processed count "
                "does not match the ingestion result."
            )

        if (
            indexing_run.chunks_created
            != result.stored_chunk_count
        ):
            raise AssertionError(
                "Indexing-run chunk count "
                "does not match the ingestion result."
            )

        print("Persistent Indexing Records")
        print("-" * 50)
        print(
            f"Knowledge source ID: "
            f"{persistent_source.id}"
        )
        print(
            f"Indexing run ID: {indexing_run.id}"
        )
        print(
            f"Indexing run status: "
            f"{indexing_run.status}"
        )
        print()

        print(
            "Repository ingestion and persistent "
            "indexing records validated successfully."
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()