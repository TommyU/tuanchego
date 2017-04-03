# -*- coding:utf-8 -*-
from .models import Car,Brand
from django.core.paginator import Paginator

def _get_suggested_cars():
	ret =[]
	return ret

def db_get_cars(price='', size='', brand=-1, displacement='', gearbox='', country='', page_index=1, page_size=24):
	queryset = Car.objects.all()
	if price:
		queryset = queryset.filter(price_level=price)
	if size:
		queryset = queryset.filter(size=size)
	if brand and brand!=-1:
		queryset = queryset.filter(brand=brand)
	if displacement:
		queryset = queryset.filter(displacement=displacement)
	if gearbox:
		queryset = queryset.filter(gearbox=gearbox)
	if country:
		queryset = queryset.filter(origin=country)
	cnt = queryset.count()
	pager = Paginator(queryset, page_size)
	try:
		page = pager.page(page_index)
	except:
		page = pager.page(1)
	car_list = []
	for line in page:
		car_list.append({
				  'name':line.name,
				  'joined_cnt':0,#TODO
				  'logo':line.logo_url,
				  'img':line.img_path,
				  'desc':line.description
			})
	ret= {
		'cnt':cnt,
		'page_index':page_index, 
		'page_size':page_size, 
		'page_count':int((cnt+page_size-1)/page_size),
		'cars':car_list
	}
	if not cnt:
		ret.update({'sg_cars':_get_suggested_cars()})
	return ret

def db_get_car_info(level, brand_id=-1, page_index=1, page_size=100):
	if level=='car':
		queryset = Car.objects.all().filter(brand=brand_id)
	else:
		queryset = Brand.objects.all()
	paginator = Paginator(queryset, page_size)
	try:
		page = paginator.page(page_index)
	except:
		page = paginator.page(1)

	lines=[]
	for line in page:
		data_dct = {
			'bid':line.brand and line.brand.id if level=='car' else line.id,
			'id':line.id,
			'name':line.name
		}
		if level=='brand':
			data_dct.update({
					'initail':line.initial,
					'logo':line.logo_url
				})

		lines.append(data_dct)
	cnt= queryset.count()
	return {
		'cnt':cnt,
		'lv':level,
		'page_size':page_size,
		'page_index':page_index,
		'page_count':int((cnt+page_size-1)/page_size),
		'lines':lines
	}

def db_get_elec_cars(city_id, page_index=1, page_size=24):
	queryset = Car.objects.all().filter(size='1')
	#TODO: by city

	paginator = Paginator(queryset, page_size)
	try:
		page = paginator.page(page_index)
	except:
		page = paginator.page(1)

	cnt = queryset.count()
	lines = []
	for line in page:
		lines.append({
				'car_id':line.id,
				'name':line.name
			})
	return {
		'cnt':cnt,
		'page_size':page_size,
		'page_index':page_index,
		'page_count':int((cnt+page_size-1)/page_size),
		'cars':lines
	}
