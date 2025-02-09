celery -A tasks.celery_app worker --loglevel=info --concurrency=4 -Q "reminders,deactivate_bookings,deactivate_dates,deactivate_times"
