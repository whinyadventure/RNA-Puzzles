from django.urls import path, include, re_path
from django.views.generic import FormView
from . import views
from .views import News, SignupView, index
import publications.views as plist

newspatterns = [
    path('', news.List.as_view(), name="news_list"),
    path('add', news.Create.as_view(), name="news_new"),
    re_path(r"(?P<pk>\d+)/update/$", news.Update.as_view(), name="news_update"),
    re_path(r"(?P<pk>\d+)/$", news.Detail.as_view(), name="news_details"),
    re_path(r"(?P<pk>\d+)/delete/$", news.Delete.as_view(), name="news_delete")
]

faqpattern = [
    path('', faq.List.as_view(), name="faq_list"),
    path('add', faq.Create.as_view(), name="faq_new"),
    re_path(r"(?P<pk>\d+)/update/$", faq.Update.as_view(), name="faq_update"),
    re_path(r"(?P<pk>\d+)/$", faq.Detail.as_view(), name="faq_details"),
    re_path(r"(?P<pk>\d+)/delete/$", faq.Delete.as_view(), name="faq_delete")
]

resourcespattern = [
    path('', resources.List.as_view(), name="faq_list"),
    path('add', resources.Create.as_view(), name="faq_new"),
    re_path(r"(?P<pk>\d+)/update/$", resources.Update.as_view(), name="faq_update"),
    re_path(r"(?P<pk>\d+)/$", resources.Detail.as_view(), name="faq_details"),
    re_path(r"(?P<pk>\d+)/delete/$", resources.Delete.as_view(), name="faq_delete")
]

accounts_pattern = [
    path("", include("django.contrib.auth.urls")),
    re_path(r'^signup/$', User.SignupView.as_view(), name='signup'),
    re_path(r'^signin/$', User.SigninView.as_view(), name='signin'),
    re_path(r'^profile/$', User.ProfileView.as_view(), name='profile'),
    re_path(r'^groups/$', User.GroupsListView.as_view(), name='groups'),
    re_path(r"groups/(?P<pk>\w+)", User.GroupView.as_view(), name='group_details'),
    re_path(r'^logout/$', User.log_out, name='logout')
]

urlpatterns = [
 #   path('', views.index, name='index'),
    path("news/", include(newspatterns)),
    path("accounts/", include(accounts_pattern)),
    path("faq/", include(faqpattern)),
    path("contact/", views.contactView, name="contact"),
    path("resources/", include(resourcespattern))
]
