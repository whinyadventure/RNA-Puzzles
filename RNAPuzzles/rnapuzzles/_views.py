from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView

from django import forms
from .models import *


# Create your views here.
def index(request):
    return HttpResponse(render(None, "base.html"))





