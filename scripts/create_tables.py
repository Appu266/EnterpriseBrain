from app.database import engine, Base

# Import models so SQLAlchemy knows them
from app.models.document import Document


print("Creating database tables...")

Base.metadata.create_all(bind=engine)

print("Database tables created successfully.")