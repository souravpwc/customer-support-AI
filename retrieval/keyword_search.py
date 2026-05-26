"""TF-IDF keyword search over KB documents."""
from __future__ import annotations
from typing import List, Tuple

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from retrieval.document_loader import Document, get_documents


class KeywordSearch:
    def __init__(self):
        self._docs: List[Document] = []
        self._vectorizer: TfidfVectorizer | None = None
        self._matrix = None
        self._built = False

    def _build(self):
        if self._built:
            return
        self._docs = get_documents()
        corpus = [d.text for d in self._docs]
        self._vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            max_df=0.85,
            min_df=1,
            sublinear_tf=True,
        )
        self._matrix = self._vectorizer.fit_transform(corpus)
        self._built = True

    def search(self, query: str, top_k: int = 5) -> List[Tuple[Document, float]]:
        self._build()
        q_vec = self._vectorizer.transform([query])
        scores = cosine_similarity(q_vec, self._matrix).flatten()
        top_indices = np.argsort(scores)[::-1][:top_k]
        return [(self._docs[i], float(scores[i])) for i in top_indices if scores[i] > 0]


_KW_SEARCH: KeywordSearch | None = None


def get_keyword_search() -> KeywordSearch:
    global _KW_SEARCH
    if _KW_SEARCH is None:
        _KW_SEARCH = KeywordSearch()
    return _KW_SEARCH
