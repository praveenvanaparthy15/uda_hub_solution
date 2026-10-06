import json
import re

from agentic.state import UDAState
from agentic.llm import llm


CLASSIFICATION_PROMPT = """
You are a customer support ticket classifier for CultPass.

Classify the ticket into exactly one category:
- billing
- technical
- account

Also determine:
- complexity: low, medium, or high
- priority: low, medium, or high
- confidence: number between 0 and 1

Return ONLY valid JSON in this format:

{{
  "category": "billing",
  "complexity": "low",
  "priority": "medium",
  "confidence": 0.95
}}

Ticket:
Subject: {subject}
Description: {description}
Urgency: {urgency}
"""


def _extract_json(text: str) -> dict:
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError("No JSON found in classifier response")

    return json.loads(match.group())


def classifier_node(state: UDAState) -> UDAState:
    prompt = CLASSIFICATION_PROMPT.format(
        subject=state.get("subject", ""),
        description=state.get("description", ""),
        urgency=state.get("urgency", "")
    )

    try:
        response = llm.invoke(prompt)
        result = _extract_json(response.content)

        category = result.get("category", "account").lower()

        if category not in {"billing", "technical", "account"}:
            category = "account"

        state["category"] = category
        state["complexity"] = result.get("complexity", "medium")
        state["priority"] = result.get("priority", "medium")
        state["classification_confidence"] = float(
            result.get("confidence", 0.5)
        )

    except Exception as exc:
        state["category"] = "account"
        state["complexity"] = "medium"
        state["priority"] = "medium"
        state["classification_confidence"] = 0.0

        state.setdefault("execution_log", []).append({
            "agent": "classifier",
            "action": "classification_error",
            "status": "fallback",
            "error": str(exc)
        })

    state.setdefault("execution_log", []).append({
        "agent": "classifier",
        "action": "classified_ticket",
        "category": state["category"],
        "confidence": state["classification_confidence"],
        "status": "completed"
    })

    state.setdefault("messages", []).append({
        "role": "classifier",
        "content": f"Ticket classified as {state['category']}."
    })

    return state