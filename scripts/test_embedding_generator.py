from app.embeddings.embedding_generator import EmbeddingGenerator


texts = [
    "EnterpriseBrain is an AI-powered Enterprise Knowledge Assistant.",
    "The system understands enterprise documents and answers questions."
]


generator = EmbeddingGenerator()


embeddings = generator.generate(
    texts
)


print("\nEmbedding Results\n")

for index, embedding in enumerate(embeddings):

    print(f"Text {index + 1}")
    print(f"Vector Size: {len(embedding)}")
    print(f"First 5 Values: {embedding[:5]}")
    print("-" * 50)