# -*- coding:utf-8 -*-
import time
import uuid
import datetime
import jsonschema
import traceback
import simplejson
from django.http import Http404,HttpResponse
import logging as logger
logger.basicConfig(level=logger.INFO)


def parse_param(SCHEMA, method="GET"):
	def _f(f):
		def _w(request, *a, **kw):
			try:
				if request.method!=method:
					return HttpResponse(status=403)
				if method=="GET":
					input_json = {}
					for k,v in request.GET.iterlists():
						input_json.update({k:v[0]})
				else:
					input_json = simplejson.loads(request.body)
			except:
				return HttpResponse(status=400)
			else:
				try:
					jsonschema.validate(input_json, SCHEMA)
				except jsonschema.exceptions.ValidationError,ex:
					return HttpResponse(status=400)
				else:
					return f(request, input_json, *a, **kw)
		return _w
	return _f

def log(log_result=False):
	def _f(f):
		def _w(request, *a, **kw):
			if not request.session.session_key:
				request.session.create()
				request.session.set_expiry(1200)
			common='|%s|%s|%s'%(request.session.session_key, 
				datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
				request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
				)
			try:
				ret = f(request, *a, **kw)
				logger.info("%s|%s|GET:%s|body:%s|ret:%s"%(
					common, 
					request.path, 
					request.GET, 
					request.body,
					ret if log_result else '...'
				))
				if isinstance(ret, dict):
					return HttpResponse(simplejson.dumps(ret),  content_type="application/json")
				elif isinstance(ret, HttpResponse):
					return ret
				else:
					raise Http404
			except Exception,ex:
				logger.error("%s|%s|GET:%s|body:%s|error: %s"%(
					common, 
					request.path, 
					request.GET, 
					request.body, 
					traceback.format_exc()
				))
				raise
		return _w
	return _f
