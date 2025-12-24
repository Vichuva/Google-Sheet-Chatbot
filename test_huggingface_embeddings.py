"""
Test script to verify Hugging Face embeddings work without ONNX.
This script should run successfully even if onnxruntime is uninstalled.
"""

print("=" * 80)
print("TEST 1: Verify ONNX is not installed")
print("=" * 80)

try:
    import onnxruntime
    print("❌ ONNX is still installed! Please uninstall:")
    print("   pip uninstall onnxruntime onnxruntime-gpu -y")
    exit(1)
except ImportError:
    print("✅ ONNX is not installed (as expected)")

print("\n" + "=" * 80)
print("TEST 2: Initialize SchemaVectorStore with Hugging Face embeddings")
print("=" * 80)

try:
    from schema_intelligence.chromadb_client import SchemaVectorStore
    store = SchemaVectorStore()
    print(f"✅ SchemaVectorStore initialized successfully")
    print(f"   Embedding function type: {type(store.embedding_function).__name__}")
    
    # Verify it's Hugging Face
    if "SentenceTransformer" in type(store.embedding_function).__name__:
        print("✅ Using Hugging Face embeddings (SentenceTransformer)")
    else:
        print(f"❌ Unexpected embedding type: {type(store.embedding_function).__name__}")
        exit(1)
        
except Exception as e:
    print(f"❌ Failed to initialize SchemaVectorStore: {e}")
    exit(1)

print("\n" + "=" * 80)
print("TEST 3: Rebuild schema embeddings")
print("=" * 80)

try:
    store.clear_collection()
    store.rebuild()
    count = store.count()
    print(f"✅ Schema embeddings rebuilt successfully")
    print(f"   Total schema documents: {count}")
except Exception as e:
    print(f"❌ Failed to rebuild schema: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\n" + "=" * 80)
print("TEST 4: Test schema retrieval")
print("=" * 80)

try:
    from schema_intelligence.hybrid_retriever import retrieve_schema
    results = retrieve_schema("What is the temperature?", top_k=3)
    print(f"✅ Schema retrieval works")
    print(f"   Retrieved {len(results)} schema items:")
    for i, item in enumerate(results, 1):
        print(f"   {i}. {item['text'][:80]}...")
except Exception as e:
    print(f"❌ Schema retrieval failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\n" + "=" * 80)
print("✅ ALL TESTS PASSED!")
print("=" * 80)
print("\nThe system successfully uses Hugging Face embeddings without ONNX.")
print("It is now Streamlit-safe and Windows-safe.")
