# -*- coding:utf-8 -*-
import xadmin
from .models import Activity,ActivityComments,Application

class ActivityAdmin(object):
    list_display = ('id','city','brand', 'serie','name','start_date','end_date','customer_qty')
    list_display_links = ('name',)

    search_fields = ['name','city','brand','serie']
    list_filter =('city','brand','serie')
    readonly_fields = ('id',)

xadmin.site.register(Activity, ActivityAdmin)

class ActivityCommentsAdmin(object):
    list_display = ('id', 'activity','user', 'DOS','serie')
    list_display_links = ('id',)

    search_fields = ['activity','user']
    list_filter =('activity','serie')
    readonly_fields = ('id',)

xadmin.site.register(ActivityComments, ActivityCommentsAdmin)

class ApplicationAdmin(object):
    list_display = ('id', 'activity','name', 'phone','way','target_brand','target_serie','target_version')
    list_display_links = ('name',)

    search_fields = ['activity','name','phone'],
    list_filter =('activity','way','target_brand','target_serie','target_color','target_time','way_check_car')
    readonly_fields = ('id',)
xadmin.site.register(Application, ApplicationAdmin)