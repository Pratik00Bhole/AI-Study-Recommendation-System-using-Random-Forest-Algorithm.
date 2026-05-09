from ..ml.data_catalog import TOPIC_CATALOG
from ..ml.nlp_engine import HybridNLPEngine

nlp_engine = HybridNLPEngine()


class RecommendationService:
    @staticmethod
    def _normalize_text(value: str) -> str:
        return str(value or "").strip().lower()

    @staticmethod
    def _topic_matches(topic_data: dict, values: list[str]) -> bool:
        topic_text = RecommendationService._normalize_text(topic_data.get("topic"))
        subject_text = RecommendationService._normalize_text(topic_data.get("subject"))
        keywords_text = " ".join(topic_data.get("keywords", [])).lower()
        for value in values:
            normalized = RecommendationService._normalize_text(value)
            if not normalized:
                continue
            if normalized in topic_text or normalized in subject_text or normalized in keywords_text:
                return True
        return False

    @staticmethod
    def _difficulty_score_boost(difficulty: str) -> float:
        normalized = RecommendationService._normalize_text(difficulty)
        if normalized == "hard":
            return 0.05
        if normalized == "medium":
            return 0.03
        return 0.01

    @staticmethod
    def _tokenize(value: str) -> list[str]:
        return [token for token in RecommendationService._normalize_text(value).replace("&", " ").split() if token]

    @staticmethod
    def _is_catalog_match_for_subject(topic_data: dict, subject_name: str) -> bool:
        normalized_subject = RecommendationService._normalize_text(subject_name)
        if not normalized_subject:
            return False

        normalized_catalog_subject = RecommendationService._normalize_text(topic_data.get("subject"))
        if normalized_subject == normalized_catalog_subject:
            return True

        subject_tokens = set(RecommendationService._tokenize(normalized_subject))
        catalog_subject_tokens = set(RecommendationService._tokenize(normalized_catalog_subject))

        if len(subject_tokens) > 1 and subject_tokens.issubset(catalog_subject_tokens):
            return True

        topic_tokens = set(RecommendationService._tokenize(topic_data.get("topic", "")))
        if subject_tokens and subject_tokens.issubset(topic_tokens):
            return True

        keyword_tokens = {
            RecommendationService._normalize_text(keyword)
            for keyword in topic_data.get("keywords", [])
            if RecommendationService._normalize_text(keyword)
        }
        if normalized_subject in keyword_tokens:
            return True

        return False

    @staticmethod
    def _compute_personalization_boost(
        topic_data: dict,
        weak_topics: list[str],
        skills: list[str],
        interests: list[str],
        marks: dict,
        subject_levels: dict,
        progress_entries: list[dict],
    ) -> float:
        boost = 0.0

        if RecommendationService._topic_matches(topic_data, weak_topics):
            boost += 0.35

        if RecommendationService._topic_matches(topic_data, interests):
            boost += 0.2

        if RecommendationService._topic_matches(topic_data, skills):
            boost += 0.15

        for subject_name, mark in marks.items():
            if not RecommendationService._topic_matches(topic_data, [subject_name]):
                continue

            try:
                numeric_mark = float(mark)
            except (TypeError, ValueError):
                numeric_mark = 0.0

            if numeric_mark < 50:
                boost += 0.3
            elif numeric_mark < 70:
                boost += 0.2
            elif numeric_mark < 85:
                boost += 0.1
            else:
                boost -= 0.05

        for subject_name, level in subject_levels.items():
            if not RecommendationService._topic_matches(topic_data, [subject_name]):
                continue

            normalized_level = RecommendationService._normalize_text(level)
            if normalized_level == "low":
                boost += 0.2
            elif normalized_level == "average":
                boost += 0.1
            elif normalized_level == "good":
                boost -= 0.03

        topic_name = RecommendationService._normalize_text(topic_data.get("topic"))
        for entry in progress_entries:
            task_text = RecommendationService._normalize_text(entry.get("task"))
            status = RecommendationService._normalize_text(entry.get("status"))
            if not task_text or topic_name not in task_text:
                continue

            if status == "completed":
                boost -= 0.25
            else:
                boost += 0.1

        boost += RecommendationService._difficulty_score_boost(topic_data.get("difficulty"))
        return boost

    @staticmethod
    def _build_profile_query(weak_topics: list[str], skills: list[str], interests: list[str]) -> str:
        query_parts = weak_topics + interests + skills
        if query_parts:
            return " ".join(query_parts)
        return "personalized study recommendations"

    @staticmethod
    def _is_weak_subject(subject_name: str, weak_topics: list[str]) -> bool:
        normalized_subject = RecommendationService._normalize_text(subject_name)
        return any(
            RecommendationService._normalize_text(topic) == normalized_subject
            or normalized_subject in RecommendationService._normalize_text(topic)
            or RecommendationService._normalize_text(topic) in normalized_subject
            for topic in weak_topics
            if RecommendationService._normalize_text(topic)
        )

    @staticmethod
    def _subject_need_score(subject_name: str, marks: dict, subject_levels: dict, weak_topics: list[str]) -> float:
        try:
            mark_value = float(marks.get(subject_name, 0))
        except (TypeError, ValueError):
            mark_value = 0.0

        normalized_level = RecommendationService._normalize_text(subject_levels.get(subject_name, "average"))
        level_penalty_map = {"low": 25.0, "average": 12.0, "good": 4.0}
        level_penalty = level_penalty_map.get(normalized_level, 10.0)

        weak_penalty = 18.0 if RecommendationService._is_weak_subject(subject_name, weak_topics) else 0.0
        mark_penalty = max(0.0, 100.0 - mark_value)
        return mark_penalty + level_penalty + weak_penalty

    @staticmethod
    def _subject_difficulty(mark_value: float, level_label: str) -> str:
        normalized_level = RecommendationService._normalize_text(level_label)
        if mark_value < 50 or normalized_level == "low":
            return "hard"
        if mark_value < 75 or normalized_level == "average":
            return "medium"
        return "easy"

    @staticmethod
    def _generic_subject_recommendation(subject_name: str, marks: dict, subject_levels: dict, weak_topics: list[str]) -> dict:
        try:
            mark_value = float(marks.get(subject_name, 0))
        except (TypeError, ValueError):
            mark_value = 0.0

        level_label = str(subject_levels.get(subject_name, "average"))
        difficulty = RecommendationService._subject_difficulty(mark_value, level_label)
        need_score = RecommendationService._subject_need_score(subject_name, marks, subject_levels, weak_topics)

        return {
            "topic": f"{subject_name} Improvement Plan",
            "subject": subject_name,
            "difficulty": difficulty,
            "score": round(need_score / 100.0, 4),
            "base_score": round(need_score / 100.0, 4),
            "personalization_boost": round(need_score / 100.0, 4),
            "videos": [
                {
                    "title": f"{subject_name} concept revision",
                    "url": f"https://www.youtube.com/results?search_query={str(subject_name).strip().replace(' ', '+')}+concept+revision",
                }
            ],
            "practice_questions": [
                f"Solve 5 targeted questions from your weak {subject_name} chapters.",
                f"Write a short summary of one {subject_name} topic you found difficult.",
            ],
        }

    @staticmethod
    def _catalog_item_for_subject(
        subject_name: str,
        ranked_scores_by_index: dict,
        weak_topics: list[str],
        skills: list[str],
        interests: list[str],
        marks: dict,
        subject_levels: dict,
        progress_entries: list[dict],
    ) -> dict | None:
        matching = []
        for index, topic_data in enumerate(TOPIC_CATALOG):
            if RecommendationService._is_catalog_match_for_subject(topic_data, subject_name):
                matching.append((index, topic_data))

        if not matching:
            return None

        best_index = None
        best_score = -1e9
        best_item = None
        best_base = 0.0
        best_boost = 0.0

        for index, topic_data in matching:
            base_score = float(ranked_scores_by_index.get(index, 0.0))
            personalization_boost = RecommendationService._compute_personalization_boost(
                topic_data=topic_data,
                weak_topics=weak_topics,
                skills=skills,
                interests=interests,
                marks=marks,
                subject_levels=subject_levels,
                progress_entries=progress_entries,
            )
            score = (0.6 * base_score) + (0.4 * personalization_boost)
            if score > best_score:
                best_index = index
                best_score = score
                best_item = topic_data
                best_base = base_score
                best_boost = personalization_boost

        if best_item is None:
            return None

        return {
            "_index": best_index,
            "topic": best_item["topic"],
            "subject": subject_name,
            "difficulty": best_item["difficulty"],
            "score": round(best_score, 4),
            "base_score": round(best_base, 4),
            "personalization_boost": round(best_boost, 4),
            "videos": best_item["videos"],
            "practice_questions": best_item["practice_questions"],
        }

    @staticmethod
    def recommend(
        weak_topics: list[str],
        skills: list[str],
        interests: list[str],
        top_k: int = 3,
        marks: dict | None = None,
        subject_levels: dict | None = None,
        progress_entries: list[dict] | None = None,
    ):
        marks = marks or {}
        subject_levels = subject_levels or {}
        progress_entries = progress_entries or []

        query = RecommendationService._build_profile_query(weak_topics, skills, interests)
        documents = [
            f"{item['topic']} {item['subject']} {' '.join(item['keywords'])} {item['difficulty']}"
            for item in TOPIC_CATALOG
        ]

        ranked = nlp_engine.rank_documents(query=query, documents=documents, top_k=len(TOPIC_CATALOG))
        ranked_scores_by_index = {index: float(score) for index, score in ranked}

        subjects = list(marks.keys()) or list(subject_levels.keys()) or list(weak_topics)
        if not subjects:
            subjects = [item.get("subject") for item in TOPIC_CATALOG if item.get("subject")]

        subjects_by_need = sorted(
            subjects,
            key=lambda subject_name: RecommendationService._subject_need_score(
                subject_name=subject_name,
                marks=marks,
                subject_levels=subject_levels,
                weak_topics=weak_topics,
            ),
            reverse=True,
        )

        recommendations = []
        used_topics = set()
        used_catalog_indexes = set()

        for subject_name in subjects_by_need:
            if len(recommendations) >= top_k:
                break

            catalog_recommendation = RecommendationService._catalog_item_for_subject(
                subject_name=subject_name,
                ranked_scores_by_index=ranked_scores_by_index,
                weak_topics=weak_topics,
                skills=skills,
                interests=interests,
                marks=marks,
                subject_levels=subject_levels,
                progress_entries=progress_entries,
            )

            if catalog_recommendation:
                catalog_index = catalog_recommendation.pop("_index", None)
                if catalog_recommendation["topic"] in used_topics:
                    continue
                if catalog_index is not None:
                    used_catalog_indexes.add(catalog_index)
                used_topics.add(catalog_recommendation["topic"])
                recommendations.append(catalog_recommendation)
                continue

            generic_recommendation = RecommendationService._generic_subject_recommendation(
                subject_name=subject_name,
                marks=marks,
                subject_levels=subject_levels,
                weak_topics=weak_topics,
            )
            if generic_recommendation["topic"] in used_topics:
                continue
            used_topics.add(generic_recommendation["topic"])
            recommendations.append(generic_recommendation)

        if len(recommendations) < top_k:
            for index, score in ranked:
                if len(recommendations) >= top_k:
                    break
                if index in used_catalog_indexes:
                    continue

                topic_data = TOPIC_CATALOG[index]
                if topic_data["topic"] in used_topics:
                    continue

                personalization_boost = RecommendationService._compute_personalization_boost(
                    topic_data=topic_data,
                    weak_topics=weak_topics,
                    skills=skills,
                    interests=interests,
                    marks=marks,
                    subject_levels=subject_levels,
                    progress_entries=progress_entries,
                )
                blended_score = (0.7 * float(score)) + (0.3 * personalization_boost)

                recommendations.append(
                    {
                        "topic": topic_data["topic"],
                        "subject": topic_data["subject"],
                        "difficulty": topic_data["difficulty"],
                        "score": round(blended_score, 4),
                        "base_score": round(float(score), 4),
                        "personalization_boost": round(personalization_boost, 4),
                        "videos": topic_data["videos"],
                        "practice_questions": topic_data["practice_questions"],
                    }
                )
                used_topics.add(topic_data["topic"])

        return recommendations[:top_k]
