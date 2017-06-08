#!/usr/bin/env python
#_*_coding:utf-8_*_
from django.shortcuts import render,HttpResponse

allow_list = ['nibaba','admin']

def cron_allow(request,**kwargs):
    if request.user.username in allow_list:
        return True
    else:
        return False
def check_cron_permission(fun):
    def wapper(request, *args, **kwargs):
        if cron_allow(request, **kwargs):
            return fun(request, *args, **kwargs)
        return render(request, 'forbiden.html', locals())
    return wapper