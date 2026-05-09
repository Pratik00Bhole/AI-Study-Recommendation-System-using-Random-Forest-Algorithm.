from collections import defaultdict
from ..ml.model_pipeline import StudyModelPipeline

pipeline = StudyModelPipeline()


class AIEngineService:
    @staticmethod
    def detect_topic_strengths(
        marks: dict,
        skills: list[str],
        interests: list[str],
        subject_levels: dict | None = None,
    ):
        strong_topics = []
        weak_topics = []
        analysis = defaultdict(dict)
        normalized_levels = {
            str(topic).lower(): str(level).strip().lower()
            for topic, level in (subject_levels or {}).items()
        }
        level_score_map = {
            "good": 5,
            "average": 3,
            "low": 1,
        }

        skill_count = max(len(skills), 1)

        for topic, mark in marks.items():
            topic_key = str(topic).lower()
            interest_based_score = 5 if topic_key in [item.lower() for item in interests] else 2
            level_label = normalized_levels.get(topic_key, "average")
            level_score = level_score_map.get(level_label, 3)
            interest_score = max(interest_based_score, level_score)
            classification = pipeline.classify_topic_strength(mark, skill_count, interest_score)
            analysis[topic] = {
                "mark": mark,
                "classification": classification,
                "interest_score": interest_score,
                "level": level_label,
            }

            if classification == "weak":
                weak_topics.append(topic)
            elif classification == "strong":
                strong_topics.append(topic)

        return {
            "strong_topics": strong_topics,
            "weak_topics": weak_topics,
            "analysis": dict(analysis),
        }
