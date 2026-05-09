from openai import OpenAI
from flask import current_app


class ChatbotService:
    @staticmethod
    def _local_tutor_reply(message: str, student_context: dict | None = None):
        context_hint = ""
        if student_context:
            goal = student_context.get("goal")
            pace = student_context.get("pace")
            if goal or pace:
                context_hint = f" Goal: {goal or 'general improvement'}. Pace: {pace or 'balanced'}."

        clean_message = (message or "").strip()
        if not clean_message:
            clean_message = "your topic"

        return (
            f"Let’s work on: \"{clean_message}\".{context_hint} "
            "Start with 20 minutes of concept review, then solve 3 medium problems, "
            "and finish with a 5-minute recap of mistakes and key formulas. "
            "If you want, I can break this into a day-by-day micro-plan."
        )

    @staticmethod
    def ask_tutor(message: str, student_context: dict | None = None):
        api_key = current_app.config.get("OPENAI_API_KEY")
        model_name = current_app.config.get("OPENAI_MODEL", "gpt-4o-mini")

        if not api_key:
            return {
                "reply": ChatbotService._local_tutor_reply(message, student_context),
                "source": "fallback",
            }

        try:
            client = OpenAI(api_key=api_key)
            system_prompt = (
                "You are a supportive study tutor. Give concise, actionable guidance, "
                "and adapt explanations to student level."
            )
            context_text = f"Student context: {student_context}" if student_context else ""
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"{context_text}\nQuestion: {message}"},
                ],
                temperature=0.4,
            )
            return {
                "reply": response.choices[0].message.content,
                "source": "openai",
            }
        except Exception as exc:
            return {
                "reply": ChatbotService._local_tutor_reply(message, student_context),
                "source": f"fallback-error: {str(exc)}",
            }
