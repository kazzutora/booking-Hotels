from celery import Celery
from celery.schedules import crontab

from src.config import settings

celery_instance= Celery(
    'tasks',
    broker=settings.REDIS_URL,
    include = [
        'src.tasks.tasks',

               ],
    backend = settings.REDIS_URL,
)
celery_instance.conf.beat_schedule = {
    'luboe': {
        'task': 'booking_today_checkin',
        'schedule': 5
    }
}