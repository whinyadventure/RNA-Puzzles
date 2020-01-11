from django.urls import path, include, re_path
from django.views.generic import FormView
from . import views
from .views import news, faq, resources, group, user, puzzles
import publications.views as plist

news_patterns = [
    path('', news.List.as_view(), name="news_list"),
    path('add', news.Create.as_view(), name="news_new"),
    re_path(r"(?P<pk>\d+)/update/$", news.Update.as_view(), name="news_update"),
    re_path(r"(?P<pk>\d+)/$", news.Detail.as_view(), name="news_details"),
    re_path(r"(?P<pk>\d+)/delete/$", news.Delete.as_view(), name="news_delete")
]

faq_pattern = [
    path('', faq.List.as_view(), name="faq_list"),
    path('add', faq.Create.as_view(), name="faq_new"),
    re_path(r"(?P<pk>\d+)/update/$", faq.Update.as_view(), name="faq_update"),
    re_path(r"(?P<pk>\d+)/$", faq.Detail.as_view(), name="faq_details"),
    re_path(r"(?P<pk>\d+)/delete/$", faq.Delete.as_view(), name="faq_delete")
]


resources_pattern = [
    path('', resources.List.as_view(), name="resources_list"),
    path('add', resources.Create.as_view(), name="resources_new"),
    re_path(r"(?P<pk>\d+)/update/$", resources.Update.as_view(), name="resources_update"),
    re_path(r"(?P<pk>\d+)/$", resources.Detail.as_view(), name="resources_details"),
    re_path(r"(?P<pk>\d+)/delete/$", resources.Delete.as_view(), name="resources_delete")
]
groups_pattern = [
    re_path(r'^$', group.List.as_view(), name='groups_list'),
    re_path(r'(?P<pk>\d+)/update/$', group.Update.as_view(), name='group_update'),
    re_path(r'(?P<pk>\d+)/$', group.Detail.as_view(), name='group_detail')
]

accounts_pattern = [
    path("", include("django.contrib.auth.urls")),
    re_path(r'^signup/$', user.Signup.as_view(), name='signup'),
    re_path(r'^signin/$', user.Signin.as_view(), name='signin'),
    re_path(r'^profile/$', user.Detail.as_view(), name='user_detail'),
    re_path(r'^profile/update$', user.Update.as_view(), name='user_update'),
    re_path(r'^profile/update/password$', user.PasswordUpdate.as_view(), name='user_password_update'),
    re_path(r'^reset$', user.PasswordReset.as_view(), name='user_password_reset'),
    re_path(r'^send-reset/$', user.ResetForm.reset, name='send_reset'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', user.NewPassword.as_view(), name='new_password'),
    re_path(r'^emailSend/$', user.Signup.email_send, name='email_send'),
    re_path(r'^active/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', user.Signup.activate, name="activate"),
    path("groups/", include(groups_pattern)),
    re_path(r'^logout/$', user.Signin.logout, name='logout')
]

organizer_puzzles_pattern = [
    path('', puzzles.list_organizer, name='organizer-puzzles'),
    path('create-new', puzzles.create_new, name='create-new'),
    path('create-next', puzzles.create_next, name='create-next'),
    re_path(r"(?P<pk>\d+)/update-puzzle/$", puzzles.update_puzzle_info, name='update-puzzle-info'),
    re_path(r"(?P<pk>\d+)/update-round/$", puzzles.update_challenge, name='update-challenge'),
    re_path(r"(?P<pk>\d+)/delete-puzzle/$", puzzles.PuzzleInfoDelete.as_view(), name='puzzle-info-delete'),
    re_path(r"(?P<pk>\d+)/delete-round/$", puzzles.ChallengeDelete.as_view(), name='challenge-delete'),
]

puzzles_pattern = [
    path('', puzzles.list_open, name='open-puzzles'),
    path('completed-puzzles', puzzles.list_completed, name='completed-puzzles'),
    path('my-puzzles/', include(organizer_puzzles_pattern)),
    re_path(r"(?P<pk>\d+)/download/$", puzzles.file_download, name='download-file'),
]

urlpatterns = [
    path('', views.home, name='home'),
    path("news/", include(news_patterns)),
    path("accounts/", include(accounts_pattern)),
    path("puzzles/", include(puzzles_pattern)),
    path("faq/", include(faq_pattern)),
    path("contact/", views.contactView, name="contact"),
    path("resources/", include(resources_pattern))
]
