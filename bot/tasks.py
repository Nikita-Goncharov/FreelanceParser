from celery_periodic_tasks.celery import app
from parser.parser import parse_freelancehunt


@app.task(name='my_task')  # Fucking NAME !!!
def my_task():
    parse_freelancehunt()

