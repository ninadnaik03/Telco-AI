import json
import re


class ReasonerAgent:
    def __init__(self, llm):
        self.llm = llm

    def reason(self, query, context, metrics=None):
        # Optional metrics injection (safe)
        metrics_text = f"\nNetwork Metrics:\n{metrics}\n" if metrics else ""

        prompt = f"""
You are a telecom diagnostic AI.

STRICT RULES:
- Output ONLY valid JSON
- No markdown
- No extra text
- No explanations outside JSON

Context:
{context}

Query:
{query}
{metrics_text}

Return EXACT JSON:

{{
  "analysis": "",
  "root_cause": "",
  "confidence": 0.0,
  "recommended_actions": [],
  "explanation": {{
    "symptoms_detected": [],
    "evidence_used": [],
    "reasoning_steps": []
  }}
}}
"""

        output = self.llm.generate(prompt)

        try:
            # 🔥 Remove markdown if present
            cleaned = re.sub(r"```json|```", "", output)

            # 🔥 Extract JSON block
            match = re.search(r"\{.*\}", cleaned, re.DOTALL)

            if not match:
                raise ValueError("No JSON found")

            json_str = match.group(0)

            # 🔥 Parse JSON
            parsed = json.loads(json_str)

            # 🔥 Safety defaults
            parsed.setdefault("analysis", "")
            parsed.setdefault("root_cause", "unknown")
            parsed.setdefault("confidence", 0.3)
            parsed.setdefault("recommended_actions", [])

            parsed.setdefault("explanation", {})
            parsed["explanation"].setdefault("symptoms_detected", [])
            parsed["explanation"].setdefault("evidence_used", [])
            parsed["explanation"].setdefault("reasoning_steps", [])

            return parsed

        except Exception:
            return {
                "analysis": "Parsing failed",
                "root_cause": "unknown",
                "confidence": 0.3,
                "recommended_actions": [],
                "explanation": {
                    "symptoms_detected": [],
                    "evidence_used": [],
                    "reasoning_steps": ["Parsing failed"]
                }
            }