"""Retrieval agent — fetches relevant KB documents for the query."""
from __future__ import annotations
from typing import Any, Dict, List

from config import MAX_RETRIEVED_DOCS
from agents.state import SupportState
from retrieval.hybrid_retriever import get_retriever

# Map intents to preferred KB categories
_INTENT_CATEGORY_MAP = {
    "warranty_check": "warranty",
    "return_refund": "returns",
    "product_info": "manuals",
    "troubleshooting": "troubleshooting",
    "general_faq": "faqs",
}


def retrieve_node(state: SupportState) -> SupportState:
    """LangGraph node: retrieve relevant KB documents."""
    query = state.get("user_message", "")
    intent = state.get("intent", "general_faq")
    entities = state.get("entities", {})

    # Enrich query with entities for better retrieval
    enriched_parts = [query]
    if product := entities.get("product_name"):
        enriched_parts.append(product)
    if issue := entities.get("issue_type"):
        enriched_parts.append(issue)
    enriched_query = " ".join(enriched_parts)

    # Prefer category if intent maps to one, but always run without filter too
    preferred_category = _INTENT_CATEGORY_MAP.get(intent)

    retriever = get_retriever()

    # Always retrieve without category filter for breadth
    results = retriever.retrieve(enriched_query, top_k=MAX_RETRIEVED_DOCS)

    # If category-specific retrieval, also add category-filtered results
    if preferred_category:
        category_results = retriever.retrieve(
            enriched_query, top_k=3, category_filter=preferred_category
        )
        # Merge: prioritize category hits at top
        seen_ids = {r.doc.doc_id for r in category_results}
        merged = list(category_results)
        for r in results:
            if r.doc.doc_id not in seen_ids:
                merged.append(r)
        results = merged[:MAX_RETRIEVED_DOCS]

    # Serialize for state
    serialized: List[Dict[str, Any]] = []
    scores: List[float] = []
    for chunk in results:
        serialized.append({
            "doc_id": chunk.doc.doc_id,
            "title": chunk.doc.title,
            "category": chunk.doc.category,
            "source": chunk.doc.source_file,
            "content": chunk.doc.content[:800],
            "vector_score": round(chunk.vector_score, 4),
            "keyword_score": round(chunk.keyword_score, 4),
            "hybrid_score": round(chunk.hybrid_score, 6),
        })
        scores.append(chunk.hybrid_score)

    return {
        **state,
        "retrieved_docs": serialized,
        "retrieval_scores": scores,
    }
