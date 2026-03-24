import numpy as np

def compute_confidence(retrieval_scores, result):
    retrieval_scores = np.array(retrieval_scores)

    # Sigmoid normalization (fix negative scores)
    normalized = 1 / (1 + np.exp(-retrieval_scores))

    retrieval_conf = float(np.mean(normalized))

    llm_conf = result.get("confidence", 0.5)

    final_conf = 0.6 * retrieval_conf + 0.4 * llm_conf

    return round(final_conf, 3)