"""Troubleshooting agent — structures diagnostic steps using KB content."""
from __future__ import annotations
from typing import List

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from config import OPENAI_API_KEY, LLM_MODEL
from agents.state import SupportState

_llm = ChatOpenAI(model=LLM_MODEL, api_key=OPENAI_API_KEY, temperature=0.1)

_SYSTEM_PROMPT = """You are TechNova's Tier-1 Technical Support Specialist.
Your task is to extract and organize troubleshooting steps from the provided knowledge base content.

Rules:
- Produce NUMBERED, ACTIONABLE steps the customer can follow RIGHT NOW.
- Be specific: include exact button presses, menu paths, and expected outcomes.
- Highlight any SAFETY WARNINGS in bold.
- End with clear escalation criteria if self-service steps fail.
- Keep steps concise but complete. Max 8 steps."""


def troubleshoot_node(state: SupportState) -> SupportState:
    """LangGraph node: extract structured troubleshooting steps from KB."""
    user_message = state.get("user_message", "")
    retrieved_docs = state.get("retrieved_docs", [])
    entities = state.get("entities", {})

    # Build KB context
    kb_content = ""
    for doc in retrieved_docs[:3]:  # Use top 3 docs
        if doc.get("category") in ("troubleshooting", "manuals"):
            kb_content += f"\n\n--- {doc['title']} ---\n{doc['content']}"

    if not kb_content:
        # Fallback: use all retrieved docs
        for doc in retrieved_docs[:3]:
            kb_content += f"\n\n--- {doc['title']} ---\n{doc['content']}"

    product = entities.get("product_name", "TechNova device")
    issue = entities.get("issue_type", user_message)

    prompt = f"""Customer reports: "{user_message}"

Product: {product}

Knowledge Base Content:
{kb_content or "No specific troubleshooting guides found."}

Generate structured troubleshooting steps for this issue."""

    try:
        resp = _llm.invoke([
            SystemMessage(content=_SYSTEM_PROMPT),
            HumanMessage(content=prompt),
        ])
        steps_text = resp.content
    except Exception:
        steps_text = (
            "1. Restart your device and try again.\n"
            "2. Check all cable connections.\n"
            "3. If the issue persists, contact TechNova support for further assistance."
        )

    # Parse numbered steps
    import re
    step_matches = re.findall(r"^\d+[\.\)]\s+(.+?)(?=\n\d+[\.\)]|\Z)", steps_text, re.MULTILINE | re.DOTALL)
    steps: List[str] = [s.strip() for s in step_matches] if step_matches else [steps_text]

    # Create a short summary
    summary = f"Troubleshooting guide for: {issue[:80]}"

    return {
        **state,
        "troubleshooting_steps": steps,
        "troubleshooting_summary": summary,
    }
