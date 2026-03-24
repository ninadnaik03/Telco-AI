from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch
import json
from config import MODEL_NAME, MAX_TOKENS, TEMPERATURE


class QwenAgent:
    def __init__(self, model_name=MODEL_NAME):
        print("Loading Qwen + LoRA model...")

        # Load tokenizer from LoRA folder
        self.tokenizer = AutoTokenizer.from_pretrained("models/telco-lora")

        # 🔥 IMPORTANT FIX: set pad token
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        # Load base model (CPU-safe)
        base_model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float32,   # CPU stable
            device_map=None              # NO auto offloading
        )

        # Load LoRA adapter
        self.model = PeftModel.from_pretrained(
            base_model,
            "models/telco-lora"
        )

        # 🔥 IMPORTANT: force CPU
        self.model.to("cpu")

        print("Fine-tuned model loaded successfully.")

    def build_prompt(self, issue, context):
        return f"""
You are a senior telecom network engineer with deep expertise in RAN and core networks.

Your task is to diagnose network issues using technical reasoning.

Issue:
{issue}

Relevant Context:
{context}

Instructions:
- Think step-by-step like a telecom expert
- Correlate symptoms with possible causes
- Consider multiple layers (RAN, Core, Hardware, Config)
- Identify the MOST LIKELY root cause
- Provide confidence score (0 to 1)
- Suggest a precise technical action

Output STRICTLY in JSON format (no extra text):

{{
  "analysis": "...",
  "root_cause": "...",
  "confidence": 0.0,
  "recommended_action": "..."
}}
"""

    def generate(self, prompt):
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            padding=True
        ).to("cpu")

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )

        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Remove prompt from response
        response = response.replace(prompt, "").strip()

        return response

    def parse_output(self, response):
        try:
            response = response.strip()

            # Remove markdown JSON wrappers
            if "```json" in response:
                response = response.split("```json")[1]
            if "```" in response:
                response = response.split("```")[0]

            json_start = response.find("{")
            json_end = response.rfind("}") + 1

            if json_start == -1 or json_end == -1:
                raise ValueError("No JSON found")

            json_str = response[json_start:json_end]

            parsed = json.loads(json_str)

            required_keys = ["analysis", "root_cause", "confidence", "recommended_action"]
            for key in required_keys:
                if key not in parsed:
                    raise ValueError(f"Missing key: {key}")

            return parsed

        except Exception as e:
            print(f"[WARNING] JSON parsing failed: {e}")

            return {
                "analysis": response,
                "root_cause": "Unknown",
                "confidence": 0.0,
                "recommended_action": "Manual inspection required"
            }

    def run(self, issue, context, debug=False):
        prompt = self.build_prompt(issue, context)

        if debug:
            print("\n--- PROMPT ---\n")
            print(prompt)

        response = self.generate(prompt)

        if debug:
            print("\n--- RAW RESPONSE ---\n")
            print(response)

        return self.parse_output(response)