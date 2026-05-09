from datetime import date, timedelta


class PlannerService:
    @staticmethod
    def _normalize_text(value: str) -> str:
        return str(value or "").strip().lower()

    @staticmethod
    def _extract_completed_topics(progress_entries: list[dict], recommended_topics: list[dict]) -> set[str]:
        completed_topics = set()
        for entry in progress_entries:
            if PlannerService._normalize_text(entry.get("status")) != "completed":
                continue

            task_text = PlannerService._normalize_text(entry.get("task"))
            for topic in recommended_topics:
                topic_name = topic.get("topic", "")
                if PlannerService._normalize_text(topic_name) in task_text:
                    completed_topics.add(topic_name)
        return completed_topics

    @staticmethod
    def _estimate_daily_effort(topic: dict, weak_topics: list[str], strong_topics: list[str]) -> tuple[int, int]:
        difficulty = PlannerService._normalize_text(topic.get("difficulty"))
        topic_name = PlannerService._normalize_text(topic.get("topic"))
        weak_topics_normalized = [PlannerService._normalize_text(item) for item in weak_topics]
        strong_topics_normalized = [PlannerService._normalize_text(item) for item in strong_topics]

        minutes_by_difficulty = {"easy": 30, "medium": 45, "hard": 60}
        questions_by_difficulty = {"easy": 3, "medium": 4, "hard": 5}

        minutes = minutes_by_difficulty.get(difficulty, 45)
        questions = questions_by_difficulty.get(difficulty, 3)

        if any(topic_key and topic_key in topic_name for topic_key in weak_topics_normalized):
            minutes += 15
            questions += 2

        if any(topic_key and topic_key in topic_name for topic_key in strong_topics_normalized):
            minutes -= 10
            questions -= 1

        minutes = max(20, min(90, minutes))
        questions = max(2, min(8, questions))
        return minutes, questions

    @staticmethod
    def create_daily_weekly_plan(
        recommended_topics: list[dict],
        profile: dict | None = None,
        analysis: dict | None = None,
        progress_entries: list[dict] | None = None,
    ):
        profile = profile or {}
        analysis = analysis or {}
        progress_entries = progress_entries or []

        today = date.today()
        daily_tasks = []
        weekly_tasks = []
        weak_topics = analysis.get("weak_topics", [])
        strong_topics = analysis.get("strong_topics", [])
        completed_topics = PlannerService._extract_completed_topics(progress_entries, recommended_topics)
        marks = profile.get("marks", {})
        subject_levels = profile.get("subject_levels", {})

        for index, topic in enumerate(recommended_topics):
            task_date = today + timedelta(days=index)
            minutes, questions = PlannerService._estimate_daily_effort(topic, weak_topics, strong_topics)
            topic_name = topic.get("topic", "")
            is_completed = topic_name in completed_topics

            if is_completed:
                task_text = f"Revise {topic_name} for 20 minutes and attempt 2 challenge questions"
            else:
                task_text = f"Study {topic_name} for {minutes} minutes and solve {questions} questions"

            daily_tasks.append(
                {
                    "date": task_date.isoformat(),
                    "task": task_text,
                    "topic": topic_name,
                    "type": "daily",
                    "status": "revision" if is_completed else "pending",
                }
            )

        for idx, topic in enumerate(recommended_topics):
            topic_name = topic.get("topic", "")
            subject_name = topic.get("subject", "")
            related_mark = marks.get(subject_name)
            related_level = subject_levels.get(subject_name)

            metric_note_parts = []
            if related_mark is not None:
                metric_note_parts.append(f"current mark: {related_mark}")
            if related_level:
                metric_note_parts.append(f"level: {related_level}")
            metric_note = f" ({', '.join(metric_note_parts)})" if metric_note_parts else ""

            weekly_tasks.append(
                {
                    "week": f"Week {idx + 1}",
                    "task": f"Complete module on {topic_name}, watch recommended videos, and attempt full-topic practice{metric_note}",
                    "topic": topic_name,
                    "type": "weekly",
                }
            )

        return {"daily_tasks": daily_tasks, "weekly_tasks": weekly_tasks}
