from datetime import datetime


class ProgressService:
    @staticmethod
    def build_dashboard(entries: list[dict]):
        total = len(entries)
        completed = len([entry for entry in entries if entry.get("status") == "completed"])
        completion_percentage = round((completed / total) * 100, 2) if total else 0

        by_day = {}
        for entry in entries:
            key = entry.get("date") or datetime.utcnow().date().isoformat()
            if key not in by_day:
                by_day[key] = {"completed": 0, "pending": 0}

            if entry.get("status") == "completed":
                by_day[key]["completed"] += 1
            else:
                by_day[key]["pending"] += 1

        chart_data = [{"date": day, **stats} for day, stats in sorted(by_day.items())]
        return {
            "completion_percentage": completion_percentage,
            "total_tasks": total,
            "completed_tasks": completed,
            "graph_data": chart_data,
        }
