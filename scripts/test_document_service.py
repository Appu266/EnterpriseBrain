from app.database import SessionLocal
from app.services.document_service import DocumentService


def test_create_document():

    db = SessionLocal()

    try:
        service = DocumentService()

        document = service.create_document(
            db=db,
            filename="rag_architecture.pdf",
            file_type="PDF",
            file_path="/data/documents/rag_architecture.pdf"
        )

        print("Document Created Successfully")
        print("----------------------------")
        print(f"ID: {document.id}")
        print(f"Filename: {document.filename}")
        print(f"Type: {document.file_type}")
        print(f"Status: {document.status}")

    except Exception as e:
        print("Error occurred")
        print(e)

    finally:
        db.close()


if __name__ == "__main__":
    test_create_document()