import os
import pdfplumber
import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

DOCS_FOLDER = "docs"
INDEX_FILE = "index.faiss"
CHUNKS_FILE = "chunks.pkl"
CHUNK_SIZE = 400
OVERLAP = 50

def extract_text(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
    return text

def chunk_text(text, source_name):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i+CHUNK_SIZE])
        chunks.append({"text": chunk, "source": source_name})
        i += CHUNK_SIZE - OVERLAP
    return chunks

def build_index():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    all_chunks = []

    for filename in os.listdir(DOCS_FOLDER):
        if filename.endswith(".pdf"):
            path = os.path.join(DOCS_FOLDER, filename)
            print(f"Processing: {filename}")
            text = extract_text(path)
            chunks = chunk_text(text, filename)
            all_chunks.extend(chunks)

    print(f"Total chunks: {len(all_chunks)}")
    texts = [c["text"] for c in all_chunks]
    embeddings = model.encode(texts, show_progress_bar=True)
    embeddings = np.array(embeddings).astype("float32")

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, INDEX_FILE)
    with open(CHUNKS_FILE, "wb") as f:
        pickle.dump(all_chunks, f)

    print("Index built and saved.")

if __name__ == "__main__":
    build_index()