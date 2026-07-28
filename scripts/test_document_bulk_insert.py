from datetime import datetime

from app.database import SessionLocal
from app.models.document import Document


documents = [
    {
        "filename": "employee_handbook.pdf",
        "file_type": "PDF",
        "file_path": "/data/documents/employee_handbook.pdf",
        "status": "uploaded"
    },
    {
        "filename": "company_policy.docx",
        "file_type": "DOCX",
        "file_path": "/data/documents/company_policy.docx",
        "status": "uploaded"
    },
    {
        "filename": "technical_architecture.pdf",
        "file_type": "PDF",
        "file_path": "/data/documents/technical_architecture.pdf",
        "status": "uploaded"
    },
    {
        "filename": "project_guidelines.txt",
        "file_type": "TXT",
        "file_path": "/data/documents/project_guidelines.txt",
        "status": "uploaded"
    },
    {
        "filename": "security_standards.pdf",
        "file_type": "PDF",
        "file_path": "/data/documents/security_standards.pdf",
        "status": "uploaded"
    }
]


def insert_documents():

    db = SessionLocal()

    try:
        document_objects = [
            Document(**doc)
            for doc in documents
        ]

        db.add_all(document_objects)

        db.commit()

        print("✅ 5 documents inserted successfully")

        for document in document_objects:
            print(
                f"ID: {document.id}, "
                f"Filename: {document.filename}"
            )

    except Exception as e:
        db.rollback()
        print("❌ Insert failed")
        print(e)

    finally:
        db.close()


if __name__ == "__main__":
    insert_documents()