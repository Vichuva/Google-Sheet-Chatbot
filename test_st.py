from sentence_transformers import SentenceTransformer

print("Loading model...")
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
print("Model loaded successfully!")

# Test embedding
text = "This is a test"
embedding = model.encode(text)
print(f"Embedding shape: {embedding.shape}")
print("✅ sentence-transformers works correctly!")
