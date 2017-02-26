# -*- coding:utf-8 -*-
import xadmin
from .models import City,SysParam,Content,Links

class CityAdmin(object):
    list_display = ('id','initial','name', 'sequence','is_hot')
    list_display_links = ('name',)

    search_fields = ['name','initial']
    list_filter =('is_hot',)
    readonly_fields = ('id',)

xadmin.site.register(City, CityAdmin)

class SysParamAdmin(object):
    list_display = ('id','key','value')
    list_display_links = ('key',)

    search_fields = ['key','value']
    readonly_fields = ('id',)

xadmin.site.register(SysParam, SysParamAdmin)

class ContentAdmin(object):
    list_display = ('id','title','uri','status')
    list_display_links = ('key',)

    search_fields = ['title','uri']
    list_filter=('status',)
    readonly_fields = ('id',)

xadmin.site.register(Content, ContentAdmin)

class LinksAdmin(object):
    list_display = ('id','city', 'position','link_type','target_url','content_text')
    list_display_links = ('key',)

    search_fields = ['target_url','content_text']
    list_filter=('city','link_type')
    readonly_fields = ('id',)

xadmin.site.register(Links, LinksAdmin)