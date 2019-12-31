from django.urls import path, include, re_path
from django.views.generic import FormView
from . import views
from .views import news, faq, resources, user
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
groups_pattern = [
    re_path(r'^$', user.GroupsListView.as_view(), name='groups_list'),
    re_path(r'(?P<pk>\d+)/^$', user.GroupDetail.as_view(), name='group_detail')
]

accounts_pattern = [
    path("", include("django.contrib.auth.urls")),
    re_path(r'^signup/$', user.SignupView.as_view(), name='signup'),
    re_path(r'^signin/$', user.SigninView.as_view(), name='signin'),
    re_path(r'^profile/$', user.ProfileView.as_view(), name='profile'),
    re_path(r'^logout/$', user.logOut, name='logout'),
    re_path(r'^emailSend/$', user.email_send, name='email_send'),
    re_path(r'^active/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', user.activate, name="activate"),
    path("groups/",include(groups_pattern))

]

urlpatterns = [
 #   path('', views.index, name='index'),
    path("news/", include(newspatterns)),
    path("accounts/", include(accounts_pattern)),
    path("faq/", include(faqpattern)),
    path("contact/", views.contactView, name="contact"),
    path("resources/", include(resourcespattern))
]
