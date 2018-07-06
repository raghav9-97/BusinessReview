import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BusinessReview.settings')

app = Celery('BusinessReview')
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
app.conf.timezone = 'Asia/Kolkata'
app.conf.beat_schedule = {
    'update-script-daily': {
        'task': 'collectdata.tasks.UpdateReviews',
        'schedule': crontab(minute=0, hour=0),
    },
    'send-mail-daily': {
        'task': 'collectdata.tasks.sendmail',
        'schedule': crontab(minute=0, hour=4),
    },
}