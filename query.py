import os
from dotenv import load_dotenv
from groq import Groq
from retrieval import build_vector_store, retrieve

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

collection, embedding_model = build_vector_store()


def ask(question):
    results = retrieve(question, collection, embedding_model, top_k=5)

    docs = results["documents"][0]
    metadatas = results["metadatas"][0]

    context_parts = []
    sources = []

    for doc, metadata in zip(docs, metadatas):
        source = metadata["source"]
        chunk_id = metadata["chunk_id"]
        sources.append(f"{source}, chunk {chunk_id}")
        context_parts.append(f"Source: {source}, chunk {chunk_id}\n{doc}")

    context = "\n\n---\n\n".join(context_parts)

    system_prompt = """
You are a grounded assistant answering questions about Wellesley professor reviews.
Use only the provided context chunks to answer.
Do not use outside knowledge.
If the context does not contain enough information, say:
"I don't have enough information in the retrieved reviews to answer that."
"""

    user_prompt = f"""
Context:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2
    )

    answer = response.choices[0].message.content

    return {
        "answer": answer,
        "sources": sorted(set(sources))
    }


if __name__ == "__main__":
    question = input("Ask a question: ")
    result = ask(question)
    print("\nAnswer:")
    print(result["answer"])
    print("\nSources:")
    for source in result["sources"]:
        print("-", source)