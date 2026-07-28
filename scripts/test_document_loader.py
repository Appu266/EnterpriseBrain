from app.ingestion.document_loader import DocumentLoader


loader = DocumentLoader()

metadata = loader.load(
    "data/documents/company_policy.txt"
)

print("\nDocument Metadata\n")

for key, value in metadata.items():
    print(f"{key}: {value}")