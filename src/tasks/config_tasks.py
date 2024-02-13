from celery import Celery
import os

celery_app = Celery(
        __name__,
        broker=os.getenv("RMQ_URL")
    )


celery_app.conf.accept_content = ['json']





