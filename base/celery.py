import os

from celery import Celery
from django.conf import settings
# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')

app = Celery('base')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
# Use Eventlet as the concurrency pool for Celery worker
# app.conf.worker_pool = 'eventlet'

# Use Eventlet as the concurrency library
app.conf.update(
    worker_pool='solo',
    task_always_eager=False ,  # Set to False for production
    worker_concurrency=3,  # Adjust the concurrency level as needed
)


# Load task modules from all registered Django apps.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
# Celery configuration settings
app.conf.broker_connection_retry = False  # Disable the old setting
app.conf.broker_connection_retry_on_startup = True  # Enable the new setting for startup retries



# @app.task(bind=True, ignore_result=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')