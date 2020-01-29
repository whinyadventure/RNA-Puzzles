import os
from celery import Celery, Task, task
from celery.utils.log import get_task_logger

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RNAPuzzles.settings')
app = Celery('rnapuzzles')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

logger = get_task_logger(__name__)
@app.task
def send_feedback_email_task(name, email, message):
    from guardian.utils import get_anonymous_user
    from rnapuzzles.models import NewsModel
    for i in range(1):
        inner.delay("ala")
    return True

@app.task
def inner(name):
    import rnapuzzles.signals
    # from rnapuzzles.models.submission import Submission
    # Submission.objects.create(content="A", challenge_id=1, user_id=1)

@app.on_after_finalize.connect
def setup_periodic_tasks(**kwargs):
    #Sending the email every hour
    from rnapuzzles.celery import opened_puzzles
    app.add_periodic_task(60*60,opened_puzzles, name='Send emails')

