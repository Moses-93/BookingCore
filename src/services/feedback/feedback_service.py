from db.repository import CRUDRepository


class FeedbackService:
    def __init__(self, crud_repository: CRUDRepository):
        self.crud_repository = crud_repository
