import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor


class StudyModelPipeline:
    def __init__(self):
        self.topic_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.performance_regressor = RandomForestRegressor(n_estimators=200, random_state=42)
        self._fit_topic_classifier()
        self._fit_performance_regressor()

    def _fit_topic_classifier(self):
        # Feature schema: [mark, skill_count, interest_match_score]
        x_train = np.array(
            [
                [35, 1, 1], [42, 1, 2], [48, 2, 1], [52, 2, 2],
                [61, 3, 3], [68, 3, 2], [74, 4, 4], [82, 5, 4],
                [88, 5, 5], [93, 6, 5],
            ]
        )
        y_train = np.array(["weak", "weak", "weak", "weak", "average", "average", "strong", "strong", "strong", "strong"])
        self.topic_classifier.fit(x_train, y_train)

    def _fit_performance_regressor(self):
        # Feature schema: [avg_mark, completed_tasks, consistency_score]
        x_train = np.array(
            [
                [45, 5, 30], [50, 8, 40], [58, 10, 45], [63, 12, 55],
                [70, 14, 65], [75, 18, 75], [82, 20, 80], [88, 24, 90],
            ]
        )
        y_train = np.array([48, 52, 58, 64, 72, 78, 85, 91])
        self.performance_regressor.fit(x_train, y_train)

    def classify_topic_strength(self, mark: float, skill_count: int, interest_score: int) -> str:
        prediction = self.topic_classifier.predict([[mark, skill_count, interest_score]])[0]
        return prediction

    def predict_performance(self, avg_mark: float, completed_tasks: int, consistency_score: float) -> float:
        prediction = self.performance_regressor.predict([[avg_mark, completed_tasks, consistency_score]])[0]
        return float(round(prediction, 2))
