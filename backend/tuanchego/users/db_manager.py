# -*- coding:utf-8 -*-
from .models import SiteUser, SmsMsg
import requests
import random
import time
def check_user(account, passwd):
	try:
		u_obj = SiteUser.objects.get(phone=account, passwd=passwd)
		return {}
	except SiteUser.DoesNotExist, ex:
		return {'error':'user_not_exist'}

def reg_user(phone, passwd):
	try:
		u = SiteUser.objects.get(phone=phone, passwd=passwd)
		return {'error':'user_already_exist'}
	except SiteUser.DoesNotExist,ex:
		u = SiteUser(phone=phone, passwd=passwd)
	u.save()
	return {}

def check_sms(phone, data):
	"""
	phone - phone number
	data - sms verification code
	"""
	try:
		sms = SmsMsg.objects.get(phone=phone, data=data)
		if sms.used:
			return {'error':'sms_used'}
		sms.used=True
		sms.save()
		return {}
	except SmsMsg.DoesNotExist,ex:
		return {'error':'sms_not_exist'}

def send_reg_sms(phone):
	"""
	send sms message to phone (for registration)
	args:
		phone - phone number
		msg - message or message template id
		data - verification code
	"""
	
	url ='http://sms.market.alicloudapi.com/singleSendSms'
	try:
		msg_obj = SmsMsg.objects.get(phone=phone,used=False, msg_type='reg')
		very_code = msg_obj.data
		is_first=False
	except SmsMsg.DoesNotExist,ex:
		very_code=random.randint(100000, 999999)
		msg_obj = SmsMsg(phone=phone, data=very_code, msg_type='reg', valid_to= int(time.time())+24*60*60 )
		msg_obj.save()
		is_first=True
	if is_first or msg_obj.valid_to <= time.time() + 180:
		data = {
			'ParamString':'{"verifyCode":"%s"}'%very_code,#TODO: 
			'RecNum':phone,
			'SignName':u'团车购',
			'TemplateCode':'SMS_60130488'#TODO: 
		}
		try:
			resp = requests.get(url, data, 
				headers={'Authorization':'APPCODE e3c58190e72a4cd3a39cb7d3454a2bb7'},
				timeout=(2,2))
		except:
			return {"error":"ali_not_available", "error_msg":"network problem"}
		else:
			ret = resp.json()
			if not ret['success']:
				return {'error':'ali_sms_failure', 'error_msg':ret.get('message','')}
	return {'phone':phone}

