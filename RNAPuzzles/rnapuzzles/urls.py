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
    path('', Puzzles.list_open, name='open-puzzles'),
    path('results', Puzzles.list_completed, name='completed-puzzles'),
    path('my-puzzles', Puzzles.list_organizer, name='organizer-puzzles'),
    path('create-new', Puzzles.create_new, name='create-new'),
    path('create-next', Puzzles.create_next, name='create-next'),
    re_path(r"(?P<pk>\d+)/download/$", Puzzles.file_download, name='download-file'),
    re_path(r"(?P<pk>\d+)/edit/$", Puzzles.edit, name='puzzle-edit'),
    re_path(r"(?P<pk>\d+)/delete-puzzle/$", Puzzles.PuzzleInfoDelete.as_view(), name='puzzle-info-delete'),
    re_path(r"(?P<pk>\d+)/delete-round/$", Puzzles.ChallengeDelete.as_view(), name='challenge-delete'),

]

urlpatterns = [
 #   path('', views.index, name='index'),
    path("news/", include(news_patterns)),
    path("accounts/", include(accounts_pattern)),
    path("puzzles/", include(puzzles_pattern)),
    path("", index),
]
