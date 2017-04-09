# -*- coding:utf-8 -*-
from .models import Activity,ActivityComments,Application
from cars.models import Car
from django.core.paginator import Paginator
import datetime
import pytz

def db_get_brand_acts(city_id, brand_id=-1, page_index=1, page_size=5):
	"""按品牌输出活动列表"""
	queryset = Activity.objects.all().filter(city=city_id, act_type='0')
	if brand_id!=-1:
		queryset = queryset.filter(brand=brand_id)
	else:
		queryset = queryset.filter(is_hot=True)

	paginator = Paginator(queryset, page_size)
	try:
		page = paginator.page(page_index)
	except:
		page = paginator.page(1)

	cnt = queryset.count()
	lines = []
	now = pytz.utc.localize(datetime.datetime.now())
	for line in page:
		hot_cars=[]
		for car in line.cars.all():
			hot_cars.append({
					'id':car.id,
					'name':car.name,
					'link':'', #TODO: reverse
				})
		lines.append({
				'brand_logo':line.brand.logo_url,
				'brand_name':line.brand.name,
				'act_name':line.name,
				'status':u'筹备中' if not line.start_date or now<=line.start_date or now else u'进行中',
				'joined_cnt':line.customer_qty or 0,
				'date':line.act_day and line.act_day.strftime('%Y-%m-%d') or '',
				'total_cut':'%.2f'%float(line.total_cut),
				'img':line.imgs.split(','),
				'link':'',#TODO:reverse()
				'hot_cars':hot_cars
			})
	return {
		'cnt':cnt,
		'page_size':page_size,
		'page_index':page_index,
		'page_count':int((cnt+page_size-1)/page_size),
		'acts':lines
	}

def db_get_car_acts(city_id, brand_id=-1,price='',size='',page_index=1, page_size=24):
	"""按车型输出活动列表"""
	queryset = Activity.objects.all().filter(city=city_id, act_type='1')
	if brand_id==-1 and not price and not size:
		queryset = queryset.filter(is_hot=True)
	else:
		cars_queryset = Car.objects.all()
		if brand_id and brand_id!=-1:
			cars_queryset = cars_queryset.filter(brand=brand_id)
		if price:
			cars_queryset = cars_queryset.filter(price=price)
		if size:
			cars_queryset = cars_queryset.filter(size=size)
		car_ids = [x.id for x in cars_queryset]
		queryset = queryset.filter(cars__in = car_ids)

	paginator = Paginator(queryset, page_size)
	try:
		page = paginator.page(page_index)
	except:
		page = paginator.page(1)

	cnt = queryset.count()
	lines = []
	now = pytz.utc.localize(datetime.datetime.now())
	for line in page:
		lines.append({
				'act_name':line.name,
				'act_status':u'筹备中' if now<=line.start_date or now else u'进行中',
				'joined_cnt':line.customer_qty or 0,
				'date':line.act_day and line.act_day.strftime('%Y-%m-%d') or '',
				'total_cut':'%.2f'%float(line.total_cut),
				'img':line.imgs.split(','),
				'link':'',#TODO:reverse()
			})
	return {
		'cnt':cnt,
		'page_size':page_size,
		'page_index':page_index,
		'page_count':int((cnt+page_size-1)/page_size),
		'acts':lines
	}

def join_acts_by_brand(application_json):
	"""按品牌进行购车"""
	try:
		act_obj = Activity.objects.get(id=application_json['aid'])
		supported_car_ids = [x.id for x in act_obj.cars.all()]
	except Activity.DoesNotExist,ex:
		return {"error":"acitivity_not_exist"}
	if int(application_json['car_id']) not  in supported_car_ids:
		return {"error":"invalid_car"}
	try:
		app_obj = Application.objects.get(
				activity=application_json['aid'],
				phone = application_json['phone']
			)
	except Application.DoesNotExist,ex:
		app_obj = Application(
			activity=application_json['aid'],
			phone = application_json['phone']
		)
	app_obj.name = application_json['name']
	app_obj.phone = application_json['phone']
	app_obj.way = application_json['way']
	app_obj.province = application_json['loc']['province']
	app_obj.city = application_json['loc']['city']
	app_obj.district = application_json['loc']['district']
	app_obj.addr = application_json['loc']['street']
	app_obj.target_brand = act_obj.brand.id#application_json['target_brand']
	app_obj.target_car = application_json['car_id']
	app_obj.target_version = application_json['version']
	app_obj.target_color = application_json['color']
	app_obj.target_time = application_json['when']
	app_obj.way_check_car = application_json['way_check_car']
	app_obj.know_cut = application_json['know_cut']
	app_obj.fenqi = application_json['fenqifenqi']
	app_obj.memo = '按品牌进行购车'
	app_obj.save()
	return {}

def db_join_acts_by_car(aid, name, phone,way):
	try:
		act_obj = Activity.objects.get(id=aid)
		supported_car_ids = [x.id for x in act_obj.cars.all()]
	except Activity.DoesNotExist,ex:
		return {"error":"acitivity_not_exist"}

	try:
		app_obj = Application.objects.get(
				activity=aid,
				phone = phone
			)
	except Application.DoesNotExist,ex:
		app_obj = Application(
			activity=aid,
			phone = phone
		)
	app_obj.name = application_json['name']
	app_obj.way = application_json['way']
	app_obj.memo = '按车型进行购车'
	app_obj.target_brand = act_obj.brand.id#application_json['target_brand']
	if supported_car_ids:# by car , only one should be configured
		app_obj.target_car = supported_car_ids[0]
	app_obj.save()
	return {}