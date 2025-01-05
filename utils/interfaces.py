from abc import ABC, abstractmethod


class InterfaceSecrets(ABC):

    @abstractmethod
    def get_secret(self, secret_name):
        pass
