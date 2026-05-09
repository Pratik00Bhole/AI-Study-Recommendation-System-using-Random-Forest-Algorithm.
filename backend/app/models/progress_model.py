from datetime import datetime
from ..extensions import db


class ProgressEntry(db.Model):
    __tablename__ = "progress"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    task = db.Column(db.Text, nullable=True)
    task_type = db.Column(db.String(20), nullable=False, default="daily")
    status = db.Column(db.String(20), nullable=False, default="pending")
    score = db.Column(db.Float, nullable=True)
    date = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)


class ProgressModel:
    @staticmethod
    def _user_id(value: str):
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _to_record(entry: ProgressEntry):
        return {
            "_id": str(entry.id),
            "user_id": str(entry.user_id),
            "task": entry.task,
            "task_type": entry.task_type,
            "status": entry.status,
            "score": entry.score,
            "date": entry.date,
            "created_at": entry.created_at,
            "completed_at": entry.completed_at,
        }

    @staticmethod
    def create_progress_entry(user_id: str, data: dict):
        normalized_user_id = ProgressModel._user_id(user_id)
        if normalized_user_id is None:
            return None

        entry = ProgressEntry(
            user_id=normalized_user_id,
            task=data.get("task"),
            task_type=data.get("task_type", "daily"),
            status=data.get("status", "pending"),
            score=data.get("score"),
            date=data.get("date"),
        )
        db.session.add(entry)
        db.session.commit()
        return ProgressModel._to_record(entry)

    @staticmethod
    def list_entries(user_id: str):
        normalized_user_id = ProgressModel._user_id(user_id)
        if normalized_user_id is None:
            return []

        entries = (
            ProgressEntry.query.filter_by(user_id=normalized_user_id)
            .order_by(ProgressEntry.created_at.desc())
            .all()
        )
        return [ProgressModel._to_record(entry) for entry in entries]

    @staticmethod
    def mark_completed(entry_id: str):
        try:
            normalized_entry_id = int(entry_id)
        except (TypeError, ValueError):
            return

        entry = db.session.get(ProgressEntry, normalized_entry_id)
        if entry is None:
            return

        entry.status = "completed"
        entry.completed_at = datetime.utcnow()
        db.session.commit()
