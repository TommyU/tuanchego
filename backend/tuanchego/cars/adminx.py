# -*- coding:utf-8 -*-
import xadmin
from .models import Brand,Serie,Version,Car

class BrandAdmin(object):
    list_display = ('id','city','name', 'initial')
    list_display_links = ('name',)

    search_fields = ['name','city','brand','serie']
    list_filter =('city',)
    readonly_fields = ('id',)

xadmin.site.register(Brand, BrandAdmin)


class SerieAdmin(object):
    list_display = ('id','brand','name')
    list_display_links = ('name',)

    search_fields = ['name']
    list_filter =('brand',)
    readonly_fields = ('id',)

xadmin.site.register(Serie, SerieAdmin)


class VersionAdmin(object):
    list_display = ('id','serie','name')
    list_display_links = ('name',)

    search_fields = ['name']
    list_filter =('serie',)
    readonly_fields = ('id',)

xadmin.site.register(Version, VersionAdmin)

class CarAdmin(object):
    list_display = ('id','brand','serie','size','name','price_level','displacement','gearbox','origin')
    list_display_links = ('name',)

    search_fields = ['name']
    list_filter =('brand','serie','price_level','gearbox','origin','size','displacement')
    readonly_fields = ('id',)

xadmin.site.register(Car, CarAdmin)

