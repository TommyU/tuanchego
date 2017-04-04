from django.conf.urls import patterns, include, url
from .views import *
urlpatterns =  patterns(
    '',
    url(r'^by_brand$', get_brand_acts, name='brand_acts_view'),
    url(r'^by_car$', get_car_acts, name='car_acts_view'),
    url(r'^join_brand$', join_acts_by_brand, name='brand_acts_view'),
    url(r'^join_car$', join_acts_by_car, name='car_acts_view'),

)