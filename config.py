import os

MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-1.5B-Instruct")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en")

FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "models/faiss_index")
DATA_PATH = os.getenv("DATA_PATH", "data/telecom_knowledge.json")

TOP_K = int(os.getenv("TOP_K", 5))
MAX_CONTEXT_LENGTH = int(os.getenv("MAX_CONTEXT_LENGTH", 3000))

TEMPERATURE = float(os.getenv("TEMPERATURE", 0.1))
MAX_NEW_TOKENS = int(os.getenv("MAX_NEW_TOKENS", 512))

RERANK_TOP_K = int(os.getenv("RERANK_TOP_K", 3))
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", 0.5))

USE_RERANKER = os.getenv("USE_RERANKER", "true").lower() == "true"
USE_FAILURE_DETECTION = os.getenv("USE_FAILURE_DETECTION", "true").lower() == "true"

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
DEVICE = os.getenv("DEVICE", "cpu")

SEED = int(os.getenv("SEED", 42))
