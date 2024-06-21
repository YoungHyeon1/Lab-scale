from celery import Celery
from app.core.config import settings
from kombu import Queue, Exchange
import structlog
import sys

logger = structlog.get_logger(__name__)
celery_app = Celery('app', broker=settings.BROKER_URL)
celery_app.conf.task_queues = (
    Queue('update', Exchange('update', type='direct'), routing_key='update', durable=True),
    Queue('predict', Exchange('predict', type='direct'), routing_key='predict', durable=True),
)


celery_app.autodiscover_tasks(['app.tasks.update_task.process_match_data'])


celery_app.conf.task_routes = {
    'tasks.update_task.process_match_data': {'queue': 'update'},
    # 'tasks.predict': {'queue': 'predict'},
}

if __name__ == '__main__':
    celery_app.start()