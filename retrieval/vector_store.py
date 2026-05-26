"""OpenAI-embedding-based vector store with on-disk cache."""
from __future__ import annotations
import pickle
import numpy as np
from typing import List, Tuple

from openai import OpenAI

from config import OPENAI_API_KEY, EMBEDDING_MODEL, EMBEDDINGS_CACHE
from retrieval.document_loader import Document, get_documents

_client = OpenAI(api_key=OPENAI_API_KEY)


def _embed_texts(texts: List[str]) -> np.ndarray:
    """Call OpenAI Embeddings API in batches of 100."""
    all_vecs: List[List[float]] = []
    batch_size = 100
    for i in range(0, len(texts), batch_size):
        batch = texts[i: i + batch_size]
        resp = _client.embeddings.create(model=EMBEDDING_MODEL, input=batch)
        all_vecs.extend([d.embedding for d in resp.data])
    return np.array(all_vecs, dtype=np.float32)


def _cosine_similarity(query_vec: np.ndarray, doc_vecs: np.ndarray) -> np.ndarray:
    q = query_vec / (np.linalg.norm(query_vec) + 1e-10)
    d = doc_vecs / (np.linalg.norm(doc_vecs, axis=1, keepdims=True) + 1e-10)
    return (d @ q).astype(float)


class VectorStore:
    def __init__(self):
        self._docs: List[Document] = []
        self._embeddings: np.ndarray | None = None
        self._loaded = False

    def _build_or_load(self):
        if self._loaded:
            return
        docs = get_documents()
        if EMBEDDINGS_CACHE.exists():
            with open(EMBEDDINGS_CACHE, "rb") as f:
                cache = pickle.load(f)
            # Invalidate cache if doc count changed
            if len(cache.get("docs", [])) == len(docs):
                self._docs = cache["docs"]
                self._embeddings = cache["embeddings"]
                self._loaded = True
                return

        # Build fresh embeddings
        texts = [d.text for d in docs]
        embeddings = _embed_texts(texts)
        self._docs = docs
        self._embeddings = embeddings
        with open(EMBEDDINGS_CACHE, "wb") as f:
            pickle.dump({"docs": docs, "embeddings": embeddings}, f)
        self._loaded = True

    def search(self, query: str, top_k: int = 5) -> List[Tuple[Document, float]]:
        self._build_or_load()
        q_vec = _embed_texts([query])[0]
        scores = _cosine_similarity(q_vec, self._embeddings)
        top_indices = np.argsort(scores)[::-1][:top_k]
        return [(self._docs[i], float(scores[i])) for i in top_indices]


# Singleton
_VECTOR_STORE: VectorStore | None = None


def get_vector_store() -> VectorStore:
    global _VECTOR_STORE
    if _VECTOR_STORE is None:
        _VECTOR_STORE = VectorStore()
    return _VECTOR_STORE
