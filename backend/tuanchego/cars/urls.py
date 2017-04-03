from django.conf.urls import patterns, include, url
from .views import *
urlpatterns =  patterns(
    '',
    url(r'^$', get_cars, name='cars_view'),
    url(r'^info$', get_car_info, name='car_info_view'),
    url(r'^elec$', get_elec_cars, name='elec_cars_view'),

)