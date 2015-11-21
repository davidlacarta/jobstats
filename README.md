# jobstats
Search jobs with infojobs api

## Demo
https://jobstats.herokuapp.com

## Heroku
Repository linked with heroku and with autodeploy

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

- Celery Beat : `celery -A collector beat -S djcelery.schedulers.DatabaseScheduler`
- Celery Worker : `celery -A collector worker -l info`
- Celery Beat and Worker: `celery -A collector worker -B -l info`

## Redis

- `redis-server`

