web: gunicorn jobstats.wsgi --log-file -
worker: celery -A collector worker -B -l info