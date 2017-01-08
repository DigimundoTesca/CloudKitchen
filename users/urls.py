from django.conf.urls import url

from users import views

app_name = 'users'

urlpatterns = [
    # index
    url(r'^$', views.index, name='index'),

    # auth
    url(r'^auth/login$', views.login, name='login'),
    url(r'^auth/logout/$', views.logout, name='logout'),

    # New Customer
    url(r'^customers/register/$', views.new_customer, name='new_customer'),
    url(r'^customers/thanks/$', views.thanks, name='thanks'),
    # url(r'^customers/register/list$', views.customers_list, name='customers_list'),

    # profile
    # url(r'^profiles/$', views.ProfileVIew, name='profiles'),

    # test
    url(r'^customers/test', views.test, name='cutomers_test'),
]