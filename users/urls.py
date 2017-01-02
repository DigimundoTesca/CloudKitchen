from django.conf.urls import url

from . import views

app_name = 'users'


urlpatterns = [
    # index
    url(r'^$', views.index, name='index'),

    # auth
    url(r'^auth/login$', views.login, name='login'),
    url(r'^auth/logout/$', views.logout, name='logout'),

    # profile
    # url(r'^profiles/$', views.ProfileVIew, name='profiles'),
]