from django.shortcuts import render
from django.http import HttpResponse
from commonlib.utils import log, parse_param
from .validator import *
from .db_manager import *

@log(log_result=False)
@parse_param(get_cars_schema, method="GET")
def get_cars(request, data ,*arg, **kwargs):
	return db_get_cars(data.get('price',''), 
		data.get('size',''), 
		data.get('brand',-1),
		data.get('displacement',''),
		data.get('gearbox',''),
		data.get('country',''),
		data.get('page_index',1),
		data.get('page_size',24)
	)

@log(log_result=False)
@parse_param(get_car_info_schema, method="GET")
def get_car_info(request, data ,*arg, **kwargs):
	return db_get_car_info(data.get('lv',''), data.get('bid',-1))

@log(log_result=True)
@parse_param(get_elec_cars_schema, method="GET")
def get_elec_cars(request, data, *args, **kwargs):
	return db_get_elec_cars(data['lid'])