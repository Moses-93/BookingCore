celery -A tasks.celery_app worker --loglevel=info --concurrency=4 -Q "reminders"
celery -A tasks.celery_app worker --loglevel=info --concurrency=6 -Q "deactivate"
