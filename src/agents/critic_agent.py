class CriticAgent:
    def __init__(self, llm):
        self.llm = llm

    def evaluate(self, result):
        prompt = f"""
Check if this telecom diagnosis is valid.

{result}

Return:
- valid (yes/no)
- reason
"""

        return self.llm.generate(prompt)