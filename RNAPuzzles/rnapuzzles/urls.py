from django.urls import path, include, re_path
from django.views.generic import FormView
from . import views
from .views import News, User, Puzzles, index
import publications.views as plist

news_patterns = [
    path('', News.List.as_view(), name="news_list"),
    path('add', News.Create.as_view(), name="news_new"),
    re_path(r"update/(?P<pk>\d+)", News.Update.as_view(), name="news_update"),
    re_path(r"(?P<pk>\d+)", News.Detail.as_view(), name="details")
]

accounts_pattern = [
    path("", include("django.contrib.auth.urls")),
    re_path(r'^signup/$', User.SignupView.as_view(), name='signup'),
    re_path(r'^signin/$', User.SigninView.as_view(), name='signin'),
]

puzzles_pattern = [
    path('', Puzzles.open_puzzles, name='open-puzzles'),
    re_path('results', Puzzles.completed_puzzles, name='completed-puzzles'),
    re_path('create-new', Puzzles.create_new, name='create-new'),
    re_path('create-next', Puzzles.create_next, name='create-next'),
]

urlpatterns = [
 #   path('', views.index, name='index'),
    path("news/", include(news_patterns)),
    path("accounts/", include(accounts_pattern)),
    path("puzzles/", include(puzzles_pattern)),
    path("", index),
]
