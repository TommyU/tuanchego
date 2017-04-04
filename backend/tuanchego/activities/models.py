# -*- coding:utf-8 -*-
from django.db import models
from data.models import BaseModel
from users.models import SiteUser
from cars.models import Brand, Serie, Car, Version
from data.models import City
# Create your models here.

class Activity(BaseModel):
	"""
	团购活动
	"""
	act_type=models.CharField(null=True, blank=True, max_length=32, default='0', choices=[('0',u'按品牌'),('1',u'按车型')])
	city = models.ForeignKey(City, null=True,blank=True, verbose_name=u'城市')
	brand = models.ForeignKey(Brand, null=True,blank=True, verbose_name=u'品牌')
	serie = models.ForeignKey(Serie, null=True,blank=True, verbose_name=u'车型')
	cars = models.ManyToManyField(Car, null=True,blank=True, verbose_name=u'车')
	name = models.CharField(max_length=64, null = True, blank=True,   verbose_name=u'名称' )
	is_hot = models.NullBooleanField(default=False, null = True, blank=True, verbose_name=u'是否热门')
	start_date = models.DateTimeField(null=True, blank=True, verbose_name=u'开始时间')
	end_date = models.DateTimeField(null=True, blank=True, verbose_name=u'结束时间')
	
	customer_qty = models.IntegerField(null=True, blank=True, default=0, verbose_name=u'参与人数')
	total_cut = models.DecimalField(default=0, max_digits=18, decimal_places=2, null=True, blank=True, verbose_name=u'总优惠（万元）')
	imgs = models.CharField(max_length=1000, default=u'活动图片', null=True, blank=True)
	act_day = models.DateField(null=True, blank=True, verbose_name=u'团购时间')
	act_place=models.CharField(max_length=128, default=u'正规4s店', verbose_name=u'团购地点')
	act_price = models.CharField(max_length=64, default=u'团购现场公布', verbose_name=u'团购价格')
	class Meta:
		verbose_name=u'团购活动'
		verbose_name_plural=u'团购活动'

class ActivityComments(BaseModel):
	"""
	团购评价
	"""
	activity = models.ForeignKey(Activity, null=True, db_index=True, verbose_name=u'团购活动', related_name="comments")
	user = models.ForeignKey(SiteUser, null=True,blank=True, verbose_name=u'用户')
	DOS = models.IntegerField(default=5, null=True, verbose_name=u'满意度')#DOS = degree of satisfaction
	comment = models.TextField(null=True, default=u'很满意!', blank=True, verbose_name=u'评价内容')
	serie = models.ForeignKey(Serie, null=True,blank=True, verbose_name=u'参团车款')

	def __str__(self):
		return self.comment
	class Meta:
		verbose_name=u'团购评价'
		verbose_name_plural=u'团购评价'

class Application(BaseModel):
	"""
	报名信息--订单信息
	"""
	#no = models.CharField(max_length=20, unique = True, verbose_name=u'报名号')
	activity = models.ForeignKey(Activity, null=True, db_index=True, verbose_name=u'团购活动', related_name="applications")
	name = models.CharField(max_length=32, null=True, blank=True, db_index=True, verbose_name=u'姓名')
	phone = models.CharField(max_length=16, null=True, blank=True, db_index=True, verbose_name=u'手机号')
	way = models.CharField(choices=[('0',u'换车'),('1',u'摇号'),('2',u'异地上牌'),('3',u'拍牌')], 
		max_length=12, null=True, blank=True, db_index=True, verbose_name=u'购车方式')
	
	#area
	province = models.CharField(verbose_name=u'省',blank=True,null=True, max_length=64)
	city = models.CharField(verbose_name=u'市',blank=True,null=True, max_length=64)
	district = models.CharField(verbose_name=u'区',blank=True,null=True, max_length=64)
	addr = models.CharField(verbose_name=u'街道地址',blank=True,null=True, max_length=256)
	
	#target car
	target_brand = models.ForeignKey(Brand, null=True,blank=True, verbose_name=u'意向品牌')
	target_car = models.ForeignKey(Car, null=True,blank=True, verbose_name=u'意向车型')
	target_version = models.ForeignKey(Version, null=True,blank=True, verbose_name=u'意向车款')
	target_color = models.CharField(max_length=2, choices=[('0',u'红'),('1',u'绿'),('2',u'蓝'),
		('3',u'黄'),('4',u'黑'),('5',u'白'),('6',u'银白')], 
		null=True, blank=True, db_index=True, verbose_name=u'车款颜色')
	target_time = models.CharField(max_length=2, choices=[
		('0',u'一周内'),
		('1',u'半个月内'),
		('2',u'一个月内'),
		('3',u'三个月内'),
		('4',u'不确定'),
		],null=True, blank=True, db_index=True, verbose_name=u'购车时间')
	way_check_car = models.CharField(max_length=2, choices=[
		('0',u'网络'),
		('1',u'4s店'),
		('2',u'其他'),
		],null=True, blank=True, db_index=True, verbose_name=u'看车途径')
	know_cut = models.IntegerField(verbose_name=u'已知优惠', default=0)

	fenqi = models.NullBooleanField(verbose_name=u'', null=True, blank=True)

	def __str__(self):
		return self.phone

	class Meta:
		verbose_name=u'报名信息'
		verbose_name_plural=u'报名信息'





