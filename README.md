# jobstats

[![Build Status](https://travis-ci.org/davidlacarta/jobstats.svg?branch=master)](https://travis-ci.org/davidlacarta/jobstats)
[![Coverage Status](https://coveralls.io/repos/davidlacarta/jobstats/badge.svg?branch=master&service=github)](https://coveralls.io/github/davidlacarta/jobstats?branch=master)
[![Join the chat at https://gitter.im/davidlacarta/jobstats](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/davidlacarta/jobstats?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

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
DJANGO_SETTINGS_MODULE : "jobstats.settings"
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
