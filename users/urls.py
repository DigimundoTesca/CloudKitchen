from django.conf.urls import url

from . import views

app_name = 'users'


urlpatterns = [
    # auth
    url(r'^$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),

    # profile
    # url(r'^profiles/$', views.ProfileVIew, name='profiles'),
]