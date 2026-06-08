import chromadb
from sentence_transformers import SentenceTransformer
from ingest import load_documents, chunk_text

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
TOP_K = 5


def build_chunks():
    documents = load_documents()
    all_chunks = []

    for doc in documents:
        chunks = chunk_text(doc["text"])

        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "id": f"{doc['source']}-{i}",
                "source": doc["source"],
                "chunk_id": i,
                "text": chunk
            })

    return all_chunks


def build_vector_store():
    chunks = build_chunks()
    model = SentenceTransformer(EMBEDDING_MODEL)

    client = chromadb.Client()

    collection = client.get_or_create_collection(
        name="professor_reviews"
    )

    texts = [chunk["text"] for chunk in chunks]
    ids = [chunk["id"] for chunk in chunks]
    metadatas = [
        {
            "source": chunk["source"],
            "chunk_id": chunk["chunk_id"]
        }
        for chunk in chunks
    ]

    embeddings = model.encode(texts).tolist()

    collection.add(
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )

    print(f"Stored {len(chunks)} chunks in ChromaDB.")

    return collection, model


def retrieve(query, collection, model, top_k=TOP_K):
    query_embedding = model.encode([query]).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results


def print_results(query, results):
    print("\n" + "=" * 80)
    print("QUERY:", query)
    print("=" * 80)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for i, doc in enumerate(documents):
        print(f"\nResult {i + 1}")
        print("Source:", metadatas[i]["source"])
        print("Chunk ID:", metadatas[i]["chunk_id"])
        print("Distance:", distances[i])
        print("Text:")
        print(doc)


def main():
    collection, model = build_vector_store()

    test_queries = [
        "What do students say about taking Vinitha Gidiraju's classes?",
        "What do people think about Samaranda Sandu's teaching?",
        "What do people think about retaking Scott Anderson's classes?",
        "What do people think about Stella Kakavouli's teaching?",
        "What do people say about Yaniv Yacoby's classes?"
    ]

    for query in test_queries:
        results = retrieve(query, collection, model)
        print_results(query, results)


if __name__ == "__main__":
    main()