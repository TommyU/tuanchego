# -*- coding:utf-8 -*-
try:
    import xadmin
    from xadmin.views import CommAdminView
    try:
        from data.xurl import data_url
    except:
        data_url=lambda x:[]
    try:
        from users.xurl import users_url
    except:
        users_url=lambda x:[]
    try:
        from cars.xurl import cars_url
    except:
        cars_url=lambda x:[]
    try:
        from activities.xurl import activities_url
    except:
        activities_url=lambda x:[]

    class GlobalSetting(object):
        site_title = u'团车购管理后台'
     
        def get_site_menu(self):
            menus = []
            menus.extend(activities_url(self))
            menus.extend(cars_url(self))
            menus.extend(users_url(self))
            menus.extend(data_url(self))
            return menus
     
    xadmin.site.register(CommAdminView, GlobalSetting)      
except:
    pass