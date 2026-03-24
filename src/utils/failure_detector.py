import numpy as np

class FailureDetector:
    def __init__(self, retrieval_threshold=0.4, confidence_threshold=0.5):
        self.retrieval_threshold = retrieval_threshold
        self.confidence_threshold = confidence_threshold

    def detect(self, query, retrieval_scores, result):
        issues = []

        # 1. Retrieval quality
        avg_score = float(np.mean(retrieval_scores))
        if avg_score < self.retrieval_threshold:
            issues.append("low_retrieval_relevance")

        # 2. LLM confidence
        llm_conf = result.get("confidence", 0.5)
        if llm_conf < self.confidence_threshold:
            issues.append("low_model_confidence")

        # 3. Missing root cause
        if result.get("root_cause", "") in ["unknown", "", None]:
            issues.append("no_clear_root_cause")

        if len(issues) > 0:
            return {
                "status": "uncertain",
                "issues": issues,
                "message": self.generate_message(issues)
            }

        return {
            "status": "confident",
            "issues": []
        }

    def generate_message(self, issues):
        if "low_retrieval_relevance" in issues:
            return "Insufficient relevant telecom knowledge retrieved."

        if "low_model_confidence" in issues:
            return "Model is uncertain about diagnosis."

        if "no_clear_root_cause" in issues:
            return "No clear root cause identified."

        return "Uncertain result."