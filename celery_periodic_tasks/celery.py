from celery import Celery
from celery.schedules import crontab


app = Celery(broker='redis://redis:6379', include=['bot.tasks'])


# celery -A celery_periodic_tasks worker --loglevel=info -B

app.conf.beat_schedule = {
    'my-task': {
        'task': 'my_task',
        'schedule': crontab(),
    },
}
