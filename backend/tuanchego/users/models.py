from django.db import models
from data.models import BaseModel
# Create your models here.
class SiteUser(BaseModel):
	"""
	网站用户
	"""
	phone = models.CharField(max_length=16, unique=True, verbose_name=u'手机号' )
	name = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'姓名')
	addr = models.CharField(max_length=256, blank=True, null=true, verbose_name=u'所在区域')
	passwd = models.CharField(max_length=64, blank=True, null=True, verbose_name=u'登录密码')

	def __str__(self):
		return self.phone or '' + self.name or ''

class SmsMsg(BaseModel):
	"""
    短信息
    """
    msg_type = models.CharField(max_length=32, choices=[('reg',u'注册'),('login',u'登录'),('reset_pw',u'重置密码'),('tip',u'提示信息'),('other',u'其他')], null=True, blank=True, verbose_name=u'类型' )
    phone = models.CharField(max_length=16, null=True, blank=True, verbose_name=u'手机号')
    msg = models.CharField(max_length=256, null=True, blank=True, verbose_name=u'信息' )
    data = models.CharField(max_length=32, null=True, blank=True, verbose_name=u'验证数据' )
    valid_to = models.DateTimeField(null=True, blank=True, verbose_name=u'失效时间')
    used =  models.BooleanField(null = True, blank=True,  verbose_name=u'验证数据是否用过了', default = False )

    def __str__(self):
    	return self.msg

class VerifyCode(BaseModel):
	"""
	图形验证码
	"""
	session_id = models.CharField(max_length=128, null=true, blank=true, verbose_name=u'浏览器会话id')
	question= models.TextField(null=True, blank=True, verbose_name=u'问题')#base64(of img)
	answer = models.CharField(max_length=8, null=true, blank=True, verbose_name=u'答案')
	used =  models.BooleanField(null = True, blank=True,  verbose_name=u'答案是否用过了', default = False )

	def __str__(self):
		return self.img_data