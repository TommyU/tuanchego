# -*- coding:utf-8 -*-
from .models import Brand,Serie,Version,Car
def cars_url(self):
	return [{
		'title': u'汽车管理', 'perm': self.get_model_perm(Brand, 'view'),
		'icon':'fa fa-cloud',
		'menus':(
			{
				'title': u'品牌',  
				'url': self.get_model_url(Brand, 'changelist'),
				'perm': self.get_model_perm(Brand, 'view'), 
			},
			{
				'title': u'型号',  
				'url': self.get_model_url(Serie, 'changelist'), 
				'perm': self.get_model_perm(Serie, 'view'), 
			},
			{
				'title': u'版本',  
				'url': self.get_model_url(Version, 'changelist'), 
				'perm': self.get_model_perm(Version, 'view'), 
			},
			{
				'title': u'汽车',  
				'url': self.get_model_url(Car, 'changelist'), 
				'perm': self.get_model_perm(Car, 'view'), 
			},
		)
	},]