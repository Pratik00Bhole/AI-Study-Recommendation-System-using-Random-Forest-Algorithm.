from ..ml.model_pipeline import StudyModelPipeline

pipeline = StudyModelPipeline()


class PredictionService:
    @staticmethod
    def predict(avg_mark: float, completed_tasks: int, consistency_score: float):
        return pipeline.predict_performance(avg_mark, completed_tasks, consistency_score)
