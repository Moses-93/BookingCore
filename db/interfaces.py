from abc import ABC, abstractmethod


class BaseCRUD(ABC):

    @abstractmethod
    async def create(self, **kwargs):
        pass

    @abstractmethod
    async def read(self, **filters):
        pass

    @abstractmethod
    async def update(self, **filters):
        pass

    @abstractmethod
    async def delete(self, **kwargs):
        pass
