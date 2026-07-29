from sqlalchemy import text

from app.database import engine


def enable_pgvector():

    with engine.connect() as connection:

        connection.execute(
            text("CREATE EXTENSION IF NOT EXISTS vector;")
        )

        connection.commit()

        print("pgvector extension enabled successfully")


if __name__ == "__main__":
    enable_pgvector()