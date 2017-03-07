# -*- coding:utf-8 -*-
from django.db import models
from data.models import BaseModel, City
# Create your models here.
class Brand(BaseModel):
	"""
	品牌
	"""
	initial = models.CharField(max_length=1,null = True, blank=True,db_index=True, verbose_name=u'首字母' )
	name = models.CharField(max_length=64, null = True, blank=True,   verbose_name=u'名称' )
	logo_url = models.CharField(max_length=128, null=True, blank=True, verbose_name=u'log uri')
	tc_url = models.CharField(max_length=128, null=True, blank=True, verbose_name=u'tc uri')
	city = models.ManyToManyField(City, verbose_name=u'城市')
	def __str__(self):
		return self.name
	class Meta:
		verbose_name=u'品牌'
		verbose_name_plural=u'品牌'

class Serie(BaseModel):
	"""
	型号
	"""
	tag = models.CharField(max_length=128, null=True, blank=True, verbose_name=u'标签')
	brand = models.ForeignKey(Brand, null=True, db_index=True, verbose_name=u'品牌')
	img_url = models.CharField(max_length=128, null=True, blank=True, verbose_name=u'图片地址')
	name = models.CharField(max_length=64, null = True, blank=True,   verbose_name=u'名称' )

	def __str__(self):
		return self.name
	class Meta:
		verbose_name=u'型号'
		verbose_name_plural=u'型号'

class Version(BaseModel):
	"""
	版本
	"""
	serie = models.ForeignKey(Serie, null=True, db_index=True, verbose_name=u'型号')
	name = models.CharField(max_length=64, null = True, blank=True,   verbose_name=u'名称' )

	def __str__(self):
		return self.name
	class Meta:
		verbose_name=u'版本'
		verbose_name_plural=u'版本'

class Car(BaseModel):
	"""
	汽车
	"""
	brand = models.ForeignKey(Brand, verbose_name=u'品牌', null=True)
	serie = models.ForeignKey(Serie, verbose_name=u'型号', null=True)
	size = models.CharField(max_length=2, verbose_name=u'', null =True, blank=True, choices=[
			('0',u'新能源'),
			('1',u'微型车'),
			('2',u'小型车'),
			('3',u'紧凑车型'),
			('4',u'中级车'),
			('5',u'豪华车'),
			('6',u'suv'),
			('7',u'MPV'),
			('8',u'跑车'),
		])
	name = models.CharField(max_length=64, null = True, blank=True, verbose_name=u'名称' )
	img_path = models.CharField(max_length=64, null = True, blank=True, verbose_name=u'图片路径' )
	price_level = models.CharField(max_length=32,null=True, blank=True, verbose_name =u'价位', choices=[
		('0,5',u'5万以下'),
		('5,10',u'5~10万'),
		('10,15',u'10~15万'),
		('15,20',u'15~20万'),
		('20,30',u'20~30万'),
		('30,9999',u'30万以上'),
		('unknown',u'不明确'),
		])
	displacement = models.DecimalField(default=0, max_digits=2, decimal_places=1, null=True, blank=True, verbose_name=u'排量(L)')
	gearbox=models.CharField(max_length=2, null = True, blank=True, verbose_name=u'变速箱', choices=[
		('0',u'手动'),
		('1',u'自动'),
		('2',u'无极变速'),
		('3',u'手自一体'),
		('4',u'双离合'),
		] )
	origin = models.CharField(max_length=2, null = True, blank=True, verbose_name=u'国别', choices=[
		('US',u'美系'),
		('DE',u'德系'),
		('01',u'进口'),
		('JP',u'日系'),
		('02',u'合资'),
		('CN',u'国产'),
		('KR',u'韩系'),
		('EU',u'欧系'),
		])

	def __str__(self):
		return self.name
	class Meta:
		verbose_name=u'汽车'
		verbose_name_plural=u'汽车'


