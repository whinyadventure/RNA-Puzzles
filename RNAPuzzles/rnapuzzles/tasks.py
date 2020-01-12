from celery import shared_task
from celery.utils.log import get_task_logger



logger=get_task_logger(__name__)

# This is the decorator which a celery worker uses
@shared_task(name="send_feedback_email_task")
def send_feedback_email_task(name,email,message):
    from rnapuzzles.models import NewsModel
    logger.info("Sent email")
    a = NewsModel.objects.create(title="Name")
    return a
#print("a")
#send_feedback_email_task.delay(None, None, None)