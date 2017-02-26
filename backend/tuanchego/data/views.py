# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View, TemplateView, RedirectView

class LoginRequiredMixin(object):
    """
    LoginRequiredMixin
    """
    @classmethod
    def as_view(cls, *args, **kwargs):
        return login_required(super(LoginRequiredMixin, cls).as_view(*args, **kwargs))

class BaseView(LoginRequiredMixin, TemplateView):
    template_name = 'base.html'