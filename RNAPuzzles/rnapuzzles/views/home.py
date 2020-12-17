from django.shortcuts import render
from ..tasks import send_feedback_email_task

def home(request):
    return render(request, 'home.html')