import random


QUESTION_TEMPLATES = {
    "easy": [
        "Define {topic} in your own words.",
        "List two real-world examples of {topic}.",
    ],
    "medium": [
        "Solve this intermediate problem related to {topic} and explain your steps.",
        "Compare two methods in {topic} and explain when to use each.",
    ],
    "hard": [
        "Design an advanced solution using {topic} with complexity analysis.",
        "Critically evaluate limitations of {topic} in practical systems.",
    ],
}


SUBJECT_QUESTION_BANK = {
    "english": {
        "easy": [
            "Identify the main idea of a short English paragraph.",
            "Write five sentences using correct punctuation and capitalization.",
        ],
        "medium": [
            "Explain the tone and theme of a short English passage with examples.",
            "Rewrite a paragraph in your own words while preserving meaning.",
        ],
        "hard": [
            "Critically analyze a passage using literary devices and evidence.",
            "Write a structured argumentative response with introduction, body, and conclusion.",
        ],
    },
    "mathematics": {
        "easy": [
            "Solve 5 basic arithmetic/algebra problems step-by-step.",
            "Find factors and multiples for the given set of numbers.",
        ],
        "medium": [
            "Solve mixed algebra and geometry problems and show all working.",
            "Apply formulas to solve word problems and verify final answers.",
        ],
        "hard": [
            "Solve multi-step higher-order problems and justify each transformation.",
            "Compare two solving strategies for the same problem and evaluate efficiency.",
        ],
    },
    "science": {
        "easy": [
            "Define key science terms and provide one real-life example for each.",
            "Draw and label a basic diagram related to the current chapter.",
        ],
        "medium": [
            "Explain a science process with cause-effect reasoning and examples.",
            "Classify given phenomena into correct scientific categories with justification.",
        ],
        "hard": [
            "Analyze an experiment setup, identify variables, and predict outcomes.",
            "Evaluate a scientific claim using evidence from concepts you learned.",
        ],
    },
    "social science": {
        "easy": [
            "List important events/terms from the chapter and define them.",
            "Match places, people, and events with correct historical/civic context.",
        ],
        "medium": [
            "Explain the impact of an event on society/economy in short points.",
            "Compare two social science concepts and state key differences.",
        ],
        "hard": [
            "Write an evidence-based answer linking causes, events, and consequences.",
            "Interpret a map/table/chart and draw reasoned conclusions.",
        ],
    },
    "hindi": {
        "easy": [
            "हिंदी पाठ का मुख्य भाव 4-5 वाक्यों में लिखिए।",
            "दिए गए शब्दों से सही वाक्य बनाइए।",
        ],
        "medium": [
            "गद्य/पद्यांश पढ़कर प्रश्नों के उत्तर अपने शब्दों में लिखिए।",
            "व्याकरण आधारित प्रश्न हल कीजिए (काल, वचन, कारक आदि)।",
        ],
        "hard": [
            "किसी विषय पर संरचित अनुच्छेद लिखिए और अलंकार/शैली का प्रयोग कीजिए।",
            "पाठ के विचारों का समालोचनात्मक विश्लेषण कीजिए।",
        ],
    },
    "computer science": {
        "easy": [
            "Define the given computing terms and provide simple examples.",
            "Trace a basic algorithm and write the output.",
        ],
        "medium": [
            "Write pseudocode for the given problem and explain each step.",
            "Differentiate between two data representation/storage approaches.",
        ],
        "hard": [
            "Design an efficient solution and discuss time-space trade-offs.",
            "Debug a faulty code snippet and justify the fix.",
        ],
    },
}


class QuestionService:
    SUBJECT_ALIASES = {
        "math": "mathematics",
        "maths": "mathematics",
        "social studies": "social science",
        "sst": "social science",
        "cs": "computer science",
        "computer basics": "computer science",
    }

    @staticmethod
    def _normalize(value: str) -> str:
        return str(value or "").strip().lower()

    @staticmethod
    def _canonical_subject(topic: str) -> str:
        normalized_topic = QuestionService._normalize(topic)
        if not normalized_topic:
            return "general"

        if normalized_topic in QuestionService.SUBJECT_ALIASES:
            return QuestionService.SUBJECT_ALIASES[normalized_topic]

        for subject_name in SUBJECT_QUESTION_BANK.keys():
            if normalized_topic == subject_name or subject_name in normalized_topic:
                return subject_name

        return normalized_topic

    @staticmethod
    def _infer_difficulty(performance_score: float):
        if performance_score < 55:
            return "easy"
        if performance_score < 75:
            return "medium"
        return "hard"

    @staticmethod
    def generate(topic: str, performance_score: float):
        level = QuestionService._infer_difficulty(performance_score)
        canonical_subject = QuestionService._canonical_subject(topic)

        subject_bank = SUBJECT_QUESTION_BANK.get(canonical_subject)
        if subject_bank and subject_bank.get(level):
            generated = list(subject_bank[level])
        else:
            generated = [template.format(topic=topic) for template in QUESTION_TEMPLATES[level]]

        random.shuffle(generated)
        return {
            "topic": topic,
            "subject": canonical_subject if canonical_subject != "general" else topic,
            "difficulty": level,
            "questions": generated,
        }
