import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer

class Retriever:
    def __init__(self, index_path, data_path, embedding_model):
        self.index = faiss.read_index(index_path)

        with open(data_path, "r") as f:
            self.data = json.load(f)

        self.embedder = SentenceTransformer(embedding_model)

    def search(self, query, top_k=5):
        q_emb = self.embedder.encode([query])
        D, I = self.index.search(np.array(q_emb), top_k)

        results = []
        for idx in I[0]:
            results.append(self.data[idx])

        return results