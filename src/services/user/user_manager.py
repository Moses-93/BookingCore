from src.services.user import UserService


class UserManager:
    def __init__(self, user_service: UserService):
        self.user_service = user_service
