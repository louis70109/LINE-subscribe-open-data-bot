web: gunicorn api:app --log-file=-
clock: python scripts/sync_to_sql.py
clock: python scripts/notify_me.py