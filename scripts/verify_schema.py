from sqlalchemy import inspect

from app.database import engine


EXPECTED_TABLES = {
    "knowledge_sources",
    "indexing_runs",
    "documents",
    "document_chunks",
}


inspector = inspect(engine)

actual_tables = set(inspector.get_table_names(schema="knowledge"))

print("Tables found in the 'knowledge' schema:")

for table_name in sorted(actual_tables):
    print(f"- {table_name}")


missing_tables = EXPECTED_TABLES - actual_tables
unexpected_tables = actual_tables - EXPECTED_TABLES

if missing_tables:
    print("\nMissing tables:")

    for table_name in sorted(missing_tables):
        print(f"- {table_name}")

if unexpected_tables:
    print("\nUnexpected tables:")

    for table_name in sorted(unexpected_tables):
        print(f"- {table_name}")

if missing_tables or unexpected_tables:
    raise SystemExit("\nSchema verification failed.")


print("\nColumns:")

for table_name in sorted(EXPECTED_TABLES):
    print(f"\nknowledge.{table_name}")

    for column in inspector.get_columns(
        table_name,
        schema="knowledge"
    ):
        nullable = "NULL" if column["nullable"] else "NOT NULL"

        print(
            f"- {column['name']}: "
            f"{column['type']} ({nullable})"
        )


print("\nSchema verification completed successfully.")