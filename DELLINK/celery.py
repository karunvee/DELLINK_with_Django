import os
from celery import chain
from celery import Celery
from celery.schedules import crontab
from django.conf import settings
# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DELLINK.settings')

app = Celery('DELLINK')
# app.conf.result_backend = 'rpc://'
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
    'delete_expired_data_Monday7hrs30': {
        'task' : 'app.tasks.delete_expired_data',
        'schedule' : crontab(hour=7, minute=30, day_of_week=1), # Executes every Monday morning at 7:30 a.m.
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
app.conf.timezone = 'Asia/Bangkok'
# Load task modules from all registered Django apps.
app.autodiscover_tasks()
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)