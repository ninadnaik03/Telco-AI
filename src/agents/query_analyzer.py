import json

class QueryAnalyzer:
    def __init__(self, llm):
        self.llm = llm

    def analyze(self, query):
        prompt = f"""
Extract structured telecom info.

Query: {query}

Return JSON:
{{
 "domain": "",
 "issue_type": "",
 "parameters": []
}}
"""

        output = self.llm.generate(prompt)

        try:
            return json.loads(output.split("{")[-1].split("}")[0] + "}")
        except:
            return {"domain": "unknown", "issue_type": "unknown", "parameters": []}