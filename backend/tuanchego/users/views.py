from django.shortcuts import render
from django.http import HttpResponse
from commonlib.utils import log, parse_param
from .validator import *
from .db_manager import *

@log(log_result=True)
@parse_param(login_schema, method="GET")
def login(request, data ,*arg, **kwargs):
	return check_user(data['phone'], data['passwd'])

@log(log_result=True)
@parse_param(reg_schema)
def reg(request, data ,*arg, **kwargs):
	return reg_user(data['phone'], data['passwd'])
	
@log(log_result=True)
@parse_param(reg_sms_schema)
def reg_sms(request, data ,*arg, **kwargs):
	return send_reg_sms(data['phone'])
