class RetrieverAgent:
    def __init__(self, retriever, reranker):
        self.retriever = retriever
        self.reranker = reranker

    def retrieve(self, query, analysis):
        queries = [query]

        if analysis["issue_type"] != "unknown":
            queries.append(analysis["issue_type"])

        docs = []
        for q in queries:
            docs.extend(self.retriever.search(q, top_k=20))  # increase recall

        reranked_docs, scores = self.reranker.rerank(query, docs, top_k=5)

        return reranked_docs, scores