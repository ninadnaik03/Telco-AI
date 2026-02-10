# System Architecture – Telco Troubleshooting Assistant

## Purpose
This document describes the high-level architecture of the Telco Troubleshooting Assistant.  
The goal is to explain how natural language inputs are transformed into structured diagnostic outputs using a combination of LLM reasoning and retrieval-based grounding.

The system is designed as a research prototype and prioritizes clarity, robustness, and modularity.

---

## High-Level Flow

1. User provides a telecom network issue in natural language.
2. Relevant domain context is retrieved using vector similarity search.
3. A large language model (LLM) analyzes the issue using the retrieved context.
4. The analysis is converted into a structured diagnosis.
5. The output is validated and saved as a machine-readable artifact.

---

## Architecture Overview
- User Input (Text)
- Context Retrieval (RAG)
- LLM Reasoning (Analysis)
- Structured Conversion (JSON)
- Validation & Repair

---

## Core Components

### 1. Input Layer
- Accepts telecom network issues written in plain English.
- No strict input format is required.
- Example:
  - "High packet loss in uplink after a recent software upgrade."

---

### 2. Context Retrieval (RAG)
- Retrieves relevant telecom-related information to ground the LLM’s reasoning.
- Implemented using:
  - Sentence embeddings
  - Vector similarity search (FAISS)
- Purpose:
  - Reduce hallucinations
  - Encourage domain-aware reasoning

---

### 3. Reasoning Engine (LLM – Analysis Stage)
- Uses an instruction-tuned large language model.
- Produces free-form analytical reasoning about:
  - Possible root causes
  - Affected components
  - Suggested actions
- This stage is intentionally unstructured to allow flexible reasoning.

---

### 4. Structuring Layer
- Converts the free-form analysis into a predefined JSON schema.
- Ensures outputs follow a consistent structure:
  - issue_summary
  - root_causes
  - confidence_score
  - explanation
  - suggested_actions
  - affected_components

---

### 5. Validation and Repair
- Handles common LLM failure modes:
  - Truncated outputs
  - Invalid JSON
  - Missing fields
- Applies:
  - Output extraction
  - Parsing checks
  - Deterministic repair when necessary

This step ensures the system always produces usable output.

---

### 6. Output Layer
- Final output is stored as a structured JSON file.
- Designed for:
  - Human inspection
  - Downstream automation
  - Future integration with monitoring tools

---

## Design Principles

- Separation of reasoning and formatting
- Robustness over perfect generation
- Explicit handling of uncertainty
- Modular design for future extensions

---

## Current Limitations

- No real-time network telemetry is used.
- Domain knowledge is limited to synthetic or simplified documents.
- The system is a prototype and not production-ready.

---

## Future Extensions

- Iterative (agent-like) troubleshooting
- Confidence-based refusal for ambiguous cases
- Evaluation against baseline models
- Fine-tuning on telecom-specific datasets

