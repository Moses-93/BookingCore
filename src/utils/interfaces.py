from abc import ABC, abstractmethod


class InterfaceSecrets(ABC):

    @abstractmethod
    def get_secret(self, secret_name):
        pass


class BaseEncryption(ABC):

    @abstractmethod
    async def encrypt(self, data: str) -> str:
        pass

    @abstractmethod
    async def decrypt(self, data: str) -> str:
        pass
