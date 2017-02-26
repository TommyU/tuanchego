# -*- coding:utf-8 -*-
from .models import Acitity,AcitityComments,Application
def activities_url(self):
	return [{
		'title': u'团购活动管理', 'perm': self.get_model_perm(Acitity, 'view'),
		'icon':'fa fa-shopping-cart',
		'menus':(
			{
				'title': u'团购活动',  
				'url': self.get_model_url(Acitity, 'changelist'),
				'perm': self.get_model_perm(Acitity, 'view'), 
			},
			{
				'title': u'团购评价',  
				'url': self.get_model_url(AcitityComments, 'changelist'), 
				'perm': self.get_model_perm(AcitityComments, 'view'), 
			},
			{
				'title': u'报名信息',  
				'url': self.get_model_url(Application, 'changelist'), 
				'perm': self.get_model_perm(Application, 'view'), 
			},
		)
	},]