# -*- coding:utf-8 -*-
from .models import City,SysParam,Content,Links
def data_url(self):
	return [{
		'title': u'基础信息管理', 'perm': self.get_model_perm(City, 'view'),
		'icon':'fa fa-th-list',
		'menus':(
			{
				'title': u'城市',  
				'url': self.get_model_url(City, 'changelist'),
				'perm': self.get_model_perm(City, 'view'), 
			},
			{
				'title': u'系统参数',  
				'url': self.get_model_url(SysParam, 'changelist'), 
				'perm': self.get_model_perm(SysParam, 'view'), 
			},
			{
				'title': u'内容页',  
				'url': self.get_model_url(Content, 'changelist'), 
				'perm': self.get_model_perm(Content, 'view'), 
			},
			{
				'title': u'链接',  
				'url': self.get_model_url(Links, 'changelist'), 
				'perm': self.get_model_perm(Links, 'view'), 
			},
		)
	},]