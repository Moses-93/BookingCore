import os
from cryptography.fernet import Fernet
from .interfaces import BaseEncryption


class EncriptionService(BaseEncryption):
    def __init__(self, key: bytes) -> str:
        self.fernet = Fernet(key)

    def encrypt(self, data: str):
        return self.fernet.encrypt(data.encode()).decode()

    def decrypt(self, data: str) -> str:
        return self.fernet.decrypt(data.encode()).decode()


encription_service = EncriptionService(os.getenv("ENCRYPTION_KEY").encode())
