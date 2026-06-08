from pathlib import Path
import re
import html
import random

DOCUMENTS_DIR = Path("documents")
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


def clean_text(text):
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def load_documents():
    documents = []

    for file_path in DOCUMENTS_DIR.glob("*.txt"):
        raw_text = file_path.read_text(encoding="utf-8")
        cleaned_text = clean_text(raw_text)

        if cleaned_text:
            documents.append({
                "source": file_path.name,
                "text": cleaned_text
            })

    return documents


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    start = 0
    step = chunk_size - overlap

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += step

    return chunks


def main():
    documents = load_documents()
    all_chunks = []

    print(f"Loaded {len(documents)} documents.")

    for doc in documents:
        chunks = chunk_text(doc["text"])

        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "source": doc["source"],
                "chunk_id": i,
                "text": chunk
            })

    print(f"Created {len(all_chunks)} chunks.")

    if not all_chunks:
        print("No chunks were created. Check that your .txt files are inside the documents folder.")
        return

    print("\nFirst 5 chunks:\n")

    for chunk in random.sample(all_chunks, min(5, len(all_chunks))):
        print("=" * 60)
        print("Source:", chunk["source"])
        print("Chunk ID:", chunk["chunk_id"])
        print(chunk["text"])
        print()


if __name__ == "__main__":
    main()