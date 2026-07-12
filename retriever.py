import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

INDEX_FILE = "index.faiss"
CHUNKS_FILE = "chunks.pkl"

model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index(INDEX_FILE)
with open(CHUNKS_FILE, "rb") as f:
    all_chunks = pickle.load(f)

def retrieve(query, top_k=4):
    query_vec = model.encode([query]).astype("float32")
    distances, indices = index.search(query_vec, top_k)
    results = []
    for i in indices[0]:
        if i < len(all_chunks):
            results.append(all_chunks[i])
    return results