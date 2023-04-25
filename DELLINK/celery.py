import os
from celery import chain
from celery import Celery
from celery.schedules import crontab
# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DELLINK.settings')

app = Celery('DELLINK')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')


app.conf.beat_schedule ={
    'data_api_3s': {
        'task' : 'app.tasks.data_api',
        'schedule' : 3,
        'options': {
            'expires': 15.0,
        },
    },
    'graph_api_6s': {
        'task' : 'app.tasks.graph_api',
        'schedule' : 6.0,
        'options': {
            'expires': 15.0,
        },
    },
    'delete_expired_data_4hrs': {
        'task' : 'app.tasks.delete_expired_data',
        'schedule' : 14400,
        'options': {
            'expires': 15.0,
        },
    },
    # 'update_utilization_start_hour': {
    #     'task' : 'app.tasks.update_utilization_per_hour',
    #     'schedule' : crontab(minute=0),
    #     'options': {
    #         'expires': 15.0,
    #     },
    # }
}

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
