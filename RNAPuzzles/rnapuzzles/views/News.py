from django import forms
from ..models import NewsModel
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView

from martor.fields import MartorFormField

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from publications.views import year as PublicationsYear
def index(request):
    return PublicationsYear(request)
    #return HttpResponse(render(request, "publications/publications.html"))



class List(ListView):
    model = NewsModel
    template_name = "news-list.html"
    paginate_by = 5

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset()
        try:
            q = self.request.GET["q"]
            queryset = queryset.filter(
                Q(title__contains=q) | Q(description__contains=q)
            )
        except:
            pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context


class Detail(DetailView):
    model = NewsModel
    template_name = "detail.html"



class From(forms.ModelForm):
    success_url = ""

    title = forms.CharField()
    description = MartorFormField()

    def __init__(self, *args, **kwargs):
        super(From, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-personal-data-form'
        self.helper.form_method = 'post'
        # self.helper.form_action = reverse('submit_form')
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = NewsModel
        fields = ["title", "description"]


class Update(UpdateView):
    model = NewsModel
    template_name = "form.html"
    success_url = ""
    form_class = From

    def get_success_url(self):
        return ""


class Create(CreateView):
    template_name = "form.html"
    success_url = ""
    model = NewsModel
    form_class = From

    def get_success_url(self):
        return ""
