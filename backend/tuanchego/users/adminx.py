# -*- coding:utf-8 -*-
import xadmin
from .models import SiteUser,SmsMsg,VerifyCode

class SiteUserAdmin(object):
    list_display = ('id','phone','name', 'addr')
    list_display_links = ('name',)

    search_fields = ['phone','name']
    readonly_fields = ('id',)

xadmin.site.register(SiteUser, SiteUserAdmin)


class SmsMsgAdmin(object):
    list_display = ('id','msg_type','phone', 'data','used')
    list_display_links = ('id',)

    search_fields = ['phone']
    list_filter=('used','msg_type')
    readonly_fields = ('id',)

xadmin.site.register(SmsMsg, SmsMsgAdmin)

class VerifyCodeAdmin(object):
    list_display = ('id','session_id','question', 'answer','used')
    list_display_links = ('id',)

    search_fields = ['question','session_id']
    list_filter=('used',)
    readonly_fields = ('id',)

xadmin.site.register(VerifyCode, VerifyCodeAdmin)