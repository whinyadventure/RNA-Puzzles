import os
from celery import Celery, Task, task
from celery.utils.log import get_task_logger

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RNAPuzzles.settings')
app = Celery('rnapuzzles')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

logger=get_task_logger(__name__)
@app.task
def send_feedback_email_task(name, email, message):
    from guardian.utils import get_anonymous_user
    from rnapuzzles.models import NewsModel
    for i in range(100):
        inner.delay("ala")
    return True

@app.task
def inner(name):
    import time
    logger.info("Start")
    time.sleep(20)
    logger.info("Stop")
    return True
@app.on_after_finalize.connect
def setup_periodic_tasks(**kwargs):
    #Sending the email every 10 Seconds
    app.add_periodic_task(10.0, send_feedback_email_task.s('Ankur','ankur@xyz.com','Hello'), name='add every 10')

