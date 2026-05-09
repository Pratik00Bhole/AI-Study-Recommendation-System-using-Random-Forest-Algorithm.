from __future__ import annotations

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

try:
    from sentence_transformers import SentenceTransformer
except Exception:  # pragma: no cover
    SentenceTransformer = None


class HybridNLPEngine:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.bert_model = None
        self._bert_loaded = False

    @staticmethod
    def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        a_norm = np.linalg.norm(a, axis=1, keepdims=True)
        b_norm = np.linalg.norm(b, axis=1, keepdims=True)
        a_norm[a_norm == 0] = 1e-9
        b_norm[b_norm == 0] = 1e-9
        return (a @ b.T) / (a_norm * b_norm.T)

    def rank_documents(self, query: str, documents: list[str], top_k: int = 5) -> list[tuple[int, float]]:
        # Lazy load BERT model on first use
        if not self._bert_loaded and SentenceTransformer:
            try:
                self.bert_model = SentenceTransformer("all-MiniLM-L6-v2")
            except Exception:
                self.bert_model = None
            self._bert_loaded = True

        corpus = [query] + documents
        tfidf_matrix = self.vectorizer.fit_transform(corpus).toarray()
        tfidf_query = tfidf_matrix[0:1]
        tfidf_docs = tfidf_matrix[1:]

        tfidf_scores = self._cosine_similarity(tfidf_query, tfidf_docs)[0]

        if self.bert_model:
            bert_embeddings = self.bert_model.encode(corpus, convert_to_numpy=True)
            bert_query = bert_embeddings[0:1]
            bert_docs = bert_embeddings[1:]
            bert_scores = self._cosine_similarity(bert_query, bert_docs)[0]
        else:
            bert_scores = tfidf_scores

        hybrid_scores = (0.55 * tfidf_scores) + (0.45 * bert_scores)
        ranked = sorted(enumerate(hybrid_scores), key=lambda x: x[1], reverse=True)
        return ranked[:top_k]
