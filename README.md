# jobstats
Statistics jobs with infojobs api

## Heroku
Repository linked with heroku and with autodeploy

Config Vars `DJANGO_SETTINGS_MODULE`:`jobstats.settings.live`

## Demo
https://jobstats.herokuapp.com

## Dashboard theme
http://startbootstrap.com/template-overviews/sb-admin-2/

## Celery

2 services
`celery -A collector beat -S djcelery.schedulers.DatabaseScheduler`
`celery -A collector worker -l info`

1 services
`celery -A collector worker -B -l info`

## Redis

`redis-server`
