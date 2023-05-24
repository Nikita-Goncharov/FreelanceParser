from celery import Celery
from celery.schedules import crontab


app = Celery(broker='redis://redis:6379', include=['bot.tasks'])


app.conf.beat_schedule = {
    'my-task': {
        'task': 'my_task',
        'schedule': crontab(),
    },
}
