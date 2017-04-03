from django.conf.urls import patterns, include, url
from .views import *
urlpatterns =  patterns(
    '',
    url(r'^login$', login, name='login_view'),
    url(r'^reg$', reg, name='reg_view'),
    url(r'^reg_sms$', reg_sms, name='reg_sms_view'),
    )