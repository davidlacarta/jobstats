web: gunicorn jobstats.wsgi --log-file -
worker: celery -A collector beat -S djcelery.schedulers.DatabaseScheduler
worker: celery -A collector worker -l info
redis: redis-server