from src.services.feedback.feedback_service import FeedbackService


class FeedbackManager:

    def __init__(self, feedback_service: FeedbackService):
        self.feedback_service = feedback_service
