#!/usr/bin/env python
#_*_ coding:utf-8_*_

from django.shortcuts import render
from app01 import models
from django.db.models import Q
from django.core.urlresolvers import resolve

def perm_online_check(request,**kwargs):
    url_obj = resolve(request.path_info)
    print("urlobj",url_obj)
    print"webusername",request.user.username
    url_name = url_obj.url_name
    print "---->urlname:",url_name
    kw = url_obj.kwargs
    print("kwargs",kw)
    print(type(kw))

    for k,v in kw.items():
        print(k,v)
        if k=='host_id':
            print'v',v
            onlinehost = models.online.objects.get(id=v)
            print("onlinehost",onlinehost)
            adf =onlinehost.sdir
            print("adf is ",adf)
            print("web submit host",adf)

            onlineinfos = models.online_permission.objects.all()
            all_list = []
            for info in onlineinfos:
                users = str(info.web_users)
                all_list.append(users)
                sdirs = str(info.src_dir).split(',')
                all_list.append(sdirs)
                print"user,sdir",users,sdirs
            print("=======",all_list)
            webuser = str(request.user.username)
            if webuser in all_list:
                num = all_list.index(webuser)
                print("num",num)
                webdir = str(adf)
                if webdir in all_list[num+1]:
                    print("--success--")
                    return True
                else:
                    print("fail")
                    return False
            else:
                print("---no include user---fail--- ")
                return False


def check_online_permission(fun):
    def wapper(request, *args, **kwargs):
        if perm_online_check(request, **kwargs):
            return fun(request, *args, **kwargs)
        return render(request, 'forbiden.html', locals())
    return wapper

