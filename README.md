# jobstats

Search jobs with infojobs api. Job offers are mapped database from api infojobs with celery task and managed from the Django admin panel. Searches are made against the database. Repository linked with heroku and with autodeploy.

## Technology Stack

- Django
- SQLite / PostgreSQL
- AngularJS
- Celery
- Redis
- Heroku
- Cloud 9

## Demo

https://jobstats.herokuapp.com

## Config Vars HEROKU

```
DJANGO_SETTINGS_MODULE : "jobstats.settings.settings"
REDIS_URL : redis addon heroku autoconfig
CLIENT_ID : client id infojobs
CLIENT_SECRET : client secret infojobs
```

## Config Vars local

```
vi ~/.bashrc
export CLIENT_ID="client id infojobs"
export CLIENT_SECRET="client secret infojobs"
export REDIS_URL="redis://127.0.0.1:6379/0"
export LOCAL="True"
source ~/.bashrc
```

## Celery

You can run the beat and worker of celery together or separately

- Celery Beat : `celery -A collector beat -S djcelery.schedulers.DatabaseScheduler`
- Celery Worker : `celery -A collector worker -l info`
- Celery Beat and Worker: `celery -A collector worker -B -l info`

## Redis

- `redis-server`

