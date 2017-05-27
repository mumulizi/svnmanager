#!/usr/bin/env python
#_*_ coding:utf-8_*_

from django.shortcuts import render
from app01 import models
from django.db.models import Q
from django.core.urlresolvers import resolve

def perm_svnproject_check(request,**kwargs):
    url_obj = resolve(request.path_info)
    print("urlobj",url_obj)
    print"webusername",request.user.username
    url_name = url_obj.url_name
    print "---->urlname:",url_name
    kw = url_obj.kwargs
    print("kwargs",kw)
   # print(type(kw))

    for k,v in kw.items():
        if k=='svn_id':
            print'v',v
            adf = str(models.svns.objects.get(id=v))
            print("web submit svnproject",adf)
            all_list = []
            sql_infos = models.svn_permission.objects.all()
            for info in sql_infos:
                users = info.web_users
                all_list.append(users)
                svn_pro = str(info.svn_projects).split(',')
                all_list.append(svn_pro)
                print("user,svn_pro",users,svn_pro)
            #print("all_list",all_list)
            webuser = str(request.user.username)
            if webuser in all_list:
                num = all_list.index(webuser)
                print"user success"
                print("num",num)
                webdir = str(adf)
                if adf in all_list[num+1]:
                    print("--success--")
                    return True
                else:
                    print("fail")
                    #print "fail user,all_list[num+1],adf",all_list,all_list[num+1],adf
                    return False
            else:
                print("---no include user---fail--- ")
                return False






def check_svnproject_permission(fun):
    def wapper(request, *args, **kwargs):
        if perm_svnproject_check(request, **kwargs):
            return fun(request, *args, **kwargs)
        return render(request, 'forbiden.html', locals())
    return wapper

