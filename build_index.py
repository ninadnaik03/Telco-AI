import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os

from config import DATA_PATH, FAISS_INDEX_PATH, EMBEDDING_MODEL


def main():
    print("🔧 Building FAISS index...")

    # Load data
    with open(DATA_PATH, "r") as f:
        data = json.load(f)

    # Convert to text
    texts = [str(item) for item in data]

    # Load embedding model
    model = SentenceTransformer(EMBEDDING_MODEL)

    print("📡 Generating embeddings...")
    embeddings = model.encode(texts, show_progress_bar=True)

    embeddings = np.array(embeddings).astype("float32")

    # Create FAISS index
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    # Save index
    os.makedirs(os.path.dirname(FAISS_INDEX_PATH), exist_ok=True)
    faiss.write_index(index, FAISS_INDEX_PATH)

    print(f"✅ FAISS index saved at {FAISS_INDEX_PATH}")


if __name__ == "__main__":
    main()