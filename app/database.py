from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.engine import URL

from config.settings import settings


# ---------------------------------
# Database URL
# ---------------------------------

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=settings.DB_USER,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    database=settings.DB_NAME
)


# ---------------------------------
# SQLAlchemy Engine
# ---------------------------------

engine = create_engine(
    DATABASE_URL,
    echo=True
)


# ---------------------------------
# Database Session
# ---------------------------------

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# ---------------------------------
# Base class for ORM models
# ---------------------------------

class Base(DeclarativeBase):
    pass


# ---------------------------------
# Database dependency
# ---------------------------------

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()