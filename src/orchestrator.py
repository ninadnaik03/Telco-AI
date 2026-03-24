from src.agents.query_analyzer import QueryAnalyzer
from src.agents.retriever_agent import RetrieverAgent
from src.agents.reasoner_agent import ReasonerAgent
from src.agents.critic_agent import CriticAgent

from src.rag.context_builder import build_context
from src.rag.reranker import Reranker

from src.utils.confidence import compute_confidence
from src.utils.failure_detector import FailureDetector


class TelecomAI:
    def __init__(self, llm, retriever):
        self.analyzer = QueryAnalyzer(llm)
        self.reranker = Reranker()
        self.retriever_agent = RetrieverAgent(retriever, self.reranker)
        self.reasoner = ReasonerAgent(llm)
        self.critic = CriticAgent(llm)
        self.failure_detector = FailureDetector()

    def run(self, query: str):
        try:
            analysis = self.analyzer.analyze(query)

            docs, scores = self.retriever_agent.retrieve(query, analysis)

            context, sources = build_context(docs)

            result = self.reasoner.reason(query, context)

            final_conf = compute_confidence(scores, result)

            failure = self.failure_detector.detect(query, scores, result)

            critique = self.critic.evaluate(result)

            return {
                "query": query,
                "query_analysis": analysis,
                "retrieved_docs_count": len(docs),
                "confidence": final_conf,
                "status": failure["status"],
                "failure_info": failure,
                "result": result,
                "explanation": result.get("explanation", {}),
                "sources_used": sources,
                "critique": critique
            }

        except Exception as err:   # ✅ FIXED VARIABLE NAME
            return {
                "error": str(err),
                "query": query
            }