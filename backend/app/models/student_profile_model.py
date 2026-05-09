from datetime import datetime
from sqlalchemy import and_
from ..extensions import db


class StudentProfile(db.Model):
    __tablename__ = "student_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    student_details = db.Column(db.JSON, nullable=False, default=dict)
    subjects = db.Column(db.JSON, nullable=False, default=list)
    marks = db.Column(db.JSON, nullable=False, default=dict)
    subject_levels = db.Column(db.JSON, nullable=False, default=dict)
    skills = db.Column(db.JSON, nullable=False, default=list)
    interests = db.Column(db.JSON, nullable=False, default=list)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class StudentProfileModel:
    @staticmethod
    def _user_id(value: str):
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _to_record(profile: StudentProfile | None):
        if not profile:
            return None
        return {
            "_id": str(profile.id),
            "user_id": str(profile.user_id),
            "student_details": profile.student_details or {},
            "subjects": profile.subjects or [],
            "marks": profile.marks or {},
            "subject_levels": profile.subject_levels or {},
            "skills": profile.skills or [],
            "interests": profile.interests or [],
            "updated_at": profile.updated_at,
        }

    @staticmethod
    def upsert_profile(user_id: str, profile_data: dict):
        normalized_user_id = StudentProfileModel._user_id(user_id)
        if normalized_user_id is None:
            return

        profile = StudentProfile.query.filter(
            and_(StudentProfile.user_id == normalized_user_id)
        ).first()

        if profile is None:
            profile = StudentProfile(user_id=normalized_user_id)
            db.session.add(profile)

        profile.student_details = profile_data.get("student_details", {})
        profile.subjects = profile_data.get("subjects", [])
        profile.marks = profile_data.get("marks", {})
        profile.subject_levels = profile_data.get("subject_levels", {})
        profile.skills = profile_data.get("skills", [])
        profile.interests = profile_data.get("interests", [])
        profile.updated_at = datetime.utcnow()

        db.session.commit()

    @staticmethod
    def get_profile(user_id: str):
        normalized_user_id = StudentProfileModel._user_id(user_id)
        if normalized_user_id is None:
            return None
        profile = StudentProfile.query.filter(
            and_(StudentProfile.user_id == normalized_user_id)
        ).first()
        return StudentProfileModel._to_record(profile)
