# -*- coding:utf-8 -*-
from .models import SiteUser,SmsMsg,VerifyCode
def users_url(self):
	return [{
		'title': u'客户管理', 'perm': self.get_model_perm(SiteUser, 'view'),
		'icon':'fa fa-phone',
		'menus':(
			{
				'title': u'客户',  
				'url': self.get_model_url(SiteUser, 'changelist'),
				'perm': self.get_model_perm(SiteUser, 'view'), 
			},
			{
				'title': u'短信息',  
				'url': self.get_model_url(SmsMsg, 'changelist'), 
				'perm': self.get_model_perm(SmsMsg, 'view'), 
			},
			{
				'title': u'图形验证码',  
				'url': self.get_model_url(VerifyCode, 'changelist'), 
				'perm': self.get_model_perm(VerifyCode, 'view'), 
			}
		)
	},]