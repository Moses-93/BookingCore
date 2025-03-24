from functools import lru_cache

from src.api.v1.api_factory import APIFactory
from src.api.v1.handler_factory import HandlerFactory
from src.core.dependencies.dependency_factory import DependencyFactory


@lru_cache()
def get_dependency_factory() -> DependencyFactory:
    return DependencyFactory()


@lru_cache()
def get_handler_factory() -> HandlerFactory:
    return HandlerFactory(get_dependency_factory())


@lru_cache()
def get_api_factory() -> APIFactory:
    return APIFactory(get_handler_factory())
