from sentence_transformers import CrossEncoder


class Reranker:
    def __init__(self, model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model = CrossEncoder(model_name)

    def rerank(self, query, docs, top_k=5):
        pairs = [(query, str(doc)) for doc in docs]

        scores = self.model.predict(pairs)

        ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)

        top_docs = [doc for doc, _ in ranked[:top_k]]
        top_scores = [float(score) for _, score in ranked[:top_k]]

        return top_docs, top_scores