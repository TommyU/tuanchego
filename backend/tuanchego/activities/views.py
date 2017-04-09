# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from commonlib.utils import log, parse_param
from .validator import *
from .db_manager import *

@log(log_result=False)
@parse_param(get_brand_acts_schema, method="POST")
def get_brand_acts(request, data ,*arg, **kwargs):
	return db_get_brand_acts(data.get('lid',''),
		data.get('brand_id',-1),
		data.get('page_index',1),
		data.get('page_size',5))

@log(log_result=False)
@parse_param(get_car_acts_schema, method="GET")
def get_car_acts(request, data, *args, **kwargs):
	return db_get_car_acts(
		data.get('brand_id',-1),
		data.get('price',''),
		data.get('size',''),
	)

@log(log_result=True)
@parse_param(join_acts_by_brand_schema, method="POST")
def join_acts_by_brand(request, data, *args, **kwargs):
	return db_join_acts_by_brand(
		{
			'aid':data.get('aid',-1),
			#----step 1-------
			'name':data.get('name',''),
			'phone':data.get('phone',''),
			'way':data.get('way',''),#
			#----step 2-------
			'loc':{
				'province':data.get('loc',{}).get('province',''),#省,
				'city':data.get('loc',{}).get('city',''),#市，
				'district':data.get('loc',{}).get('district',''),#区域，
				'street':data.get('loc',{}).get('street','')#街道
			},
			'car_id':data.get('car_id',-1),#意向车
			'version':data.get('version',''),#意向车款,
			'color':data.get('color',''),#车款颜色,
			'when':data.get('when',''),#购车时间(一周内 半个月内 一个月内 三个月内 不确定),
			'check_way':data.get('check_way',''),#看车途径（网络 4S店 其他），
			'fenqi':data.get('fenqi',None),#是否分期（是 否）,
			'known_cut':data.get('known_cut',0)#已知优惠（xx元/不确定）	
		}
	)

@log(log_result=True)
@parse_param(join_acts_by_car_schema, method="POST")
def join_acts_by_car(request, data, *args, **kwargs):
	return db_join_acts_by_car(
		data.get('aid',-1),
		data.get('name',''),
		data.get('phone',''),
		data.get('way','')#购车方式
	)