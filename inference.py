import sys
import os
import json

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from config import *
from src.utils.llm_loader import LLM
from src.rag.retriever import Retriever
from src.orchestrator import TelecomAI
from src.simulator.network_simulator import TelecomSimulator


def main():
    print("🚀 Initializing Telecom AI System...\n")

    llm = LLM(MODEL_NAME)

    retriever = Retriever(
        FAISS_INDEX_PATH,
        DATA_PATH,
        EMBEDDING_MODEL
    )

    system = TelecomAI(llm, retriever)
    simulator = TelecomSimulator()

    print("✅ System Ready!\n(Type 'exit' to quit)\n")

    while True:
        query = input("Enter telecom issue: ").strip()

        if query.lower() in ["exit", "quit"]:
            print("👋 Exiting...")
            break

        if not query:
            print("⚠️ Please enter a valid query.\n")
            continue

        try:
            sim_data = simulator.simulate(
                sinr=-5,
                cqi=3,
                interference="high",
                ue_distance=1.2
            )

            output = system.run(query)

            output["simulated_metrics"] = sim_data

            print("\n=== RESULT ===")
            print(json.dumps(output, indent=2))

        except Exception as err:   # ✅ FIXED HERE TOO
            print("\n❌ ERROR:")
            print(str(err))


if __name__ == "__main__":
    main()