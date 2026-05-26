"""Hybrid retriever: combines vector search (semantic) + TF-IDF (keyword)."""
from __future__ import annotations
from typing import List, Dict
from dataclasses import dataclass

from retrieval.document_loader import Document
from retrieval.vector_store import get_vector_store
from retrieval.keyword_search import get_keyword_search


@dataclass
class RetrievedChunk:
    doc: Document
    vector_score: float = 0.0
    keyword_score: float = 0.0
    hybrid_score: float = 0.0

    @property
    def source(self) -> str:
        return self.doc.source_file

    @property
    def snippet(self) -> str:
        return self.doc.content[:500]


class HybridRetriever:
    """Fuse vector and keyword results with Reciprocal Rank Fusion (RRF)."""

    def __init__(self, vector_weight: float = 0.6, keyword_weight: float = 0.4, rrf_k: int = 60):
        self.vector_weight = vector_weight
        self.keyword_weight = keyword_weight
        self.rrf_k = rrf_k

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        category_filter: str | None = None,
    ) -> List[RetrievedChunk]:
        fetch_k = top_k * 3

        # Run both searches
        vec_results = get_vector_store().search(query, top_k=fetch_k)
        kw_results = get_keyword_search().search(query, top_k=fetch_k)

        # Build score maps  {doc_id → (doc, v_score, kw_score)}
        combined: Dict[str, RetrievedChunk] = {}

        for rank, (doc, score) in enumerate(vec_results):
            chunk = RetrievedChunk(doc=doc, vector_score=score)
            chunk.hybrid_score += self.vector_weight * (1.0 / (self.rrf_k + rank + 1))
            combined[doc.doc_id] = chunk

        for rank, (doc, score) in enumerate(kw_results):
            if doc.doc_id in combined:
                combined[doc.doc_id].keyword_score = score
                combined[doc.doc_id].hybrid_score += self.keyword_weight * (
                    1.0 / (self.rrf_k + rank + 1)
                )
            else:
                chunk = RetrievedChunk(doc=doc, keyword_score=score)
                chunk.hybrid_score += self.keyword_weight * (1.0 / (self.rrf_k + rank + 1))
                combined[doc.doc_id] = chunk

        results = sorted(combined.values(), key=lambda x: x.hybrid_score, reverse=True)

        # Optional category filter
        if category_filter:
            results = [r for r in results if r.doc.category == category_filter]

        return results[:top_k]


_RETRIEVER: HybridRetriever | None = None


def get_retriever() -> HybridRetriever:
    global _RETRIEVER
    if _RETRIEVER is None:
        _RETRIEVER = HybridRetriever()
    return _RETRIEVER
