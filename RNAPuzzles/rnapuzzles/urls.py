from django.urls import path, include, re_path
from django.views.generic import FormView
from . import views
from .views import News, SignupView

newspatterns = [
    path('', News.List.as_view(), name="news_list"),
    path('add', News.Create.as_view(), name="news_new"),
    re_path(r"update/(?P<pk>\d+)", News.Update.as_view(), name="news_update"),
    re_path(r"(?P<pk>\d+)", News.Detail.as_view(), name="details")
]
accountspattern = [
    path("", include("django.contrib.auth.urls")),
    re_path(r'^signup/$', SignupView.as_view(), name='signup'),
]

urlpatterns = [
 #   path('', views.index, name='index'),
    path("news/", include(newspatterns)),
    path("accounts/", include(accountspattern))
]
