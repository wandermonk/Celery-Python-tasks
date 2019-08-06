from celery import Celery
from configparser import ConfigParser
from kombu import Queue
from datetime import datetime, timedelta

config = ConfigParser()

CELERY_CONFIG = {
    "CELERY_IMPORTS": ["tasks"],
    "CELERY_IGNORE_RESULT": False,
    "CELERY_TRACK_STARTED": True,
    "CELERY_DEFAULT_QUEUE": "default",
    "CELERY_QUEUES": (Queue("default"), Queue("priority")),
    "CELERY_DEFAULT_RATE_LIMIT": "20/s",
    "CELERY_RESULT_BACKEND": "amqp://",
    "CELERY_CHORD_PROPAGATES": True,
    "CELERYD_TASK_TIME_LIMIT": 7200,
    "CELERYD_POOL_RESTARTS": True,
    "CELERYD_TASK_LOG_FORMAT": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "CELERY_ANNOTATIONS": {"celery.chord_unlock": {"hard_time_limit": 360}},
    "CELERYBEAT_SCHEDULE": {
        "get_stock_info_60s": {
            "task": "tasks.reverse",
            "schedule": timedelta(seconds=60),
            "args": ("phani"),
        }
    },
}

# , backend="redis://localhost"
app = Celery("tasks", broker="amqp://guest:guest@localhost//", backend="rpc://")

app.conf.update(**CELERY_CONFIG)


@app.task
def reverse(input):
    return input[::-1]
