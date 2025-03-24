celery -A celery_worker worker --loglevel=info --concurrency=4 -Q "reminders" & echo $! > celery_reminders.pid

celery -A tasks.celery_worker worker --loglevel=info --concurrency=6 -Q "deactivate" & echo $! > celery_deactivate.pid

celery -A tasks.celery_worker beat --loglevel=info & echo $! > celery_beat.pid

echo "Celery processes started."