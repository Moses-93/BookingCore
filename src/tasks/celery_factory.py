from celery import Celery


def create_celery_app():
    celery_app = Celery("tasks")

    celery_app.config_from_object("tasks.celery_app:CeleryConfig")

    return celery_app
