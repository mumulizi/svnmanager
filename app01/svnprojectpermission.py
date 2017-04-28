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
    print(type(kw))

    for k,v in kw.items():
        if k=='svn_id':
            print'v',v
            adf = str(models.svns.objects.get(id=v))
            print("web submit host",adf)

    sql_infos = models.svn_permission.objects.all()
    # print("SQL_infos",sql_infos)
    user = []
    projects = []
    all_user_project = []
    for sql_info in sql_infos:
        sql_users = sql_info.web_users.all()

        Sql_projects = sql_info.svn_projects.all()

        # print("SQL_users",sql_users)
        # print('Sql_project',Sql_projects)
        all_user_project.append(sql_users)
        all_user_project.append(Sql_projects)
        # print('----all--',all_user_project)
        userlist = []
        projectlist = []
        for userend in sql_users:
            userlist.append(str(userend))

            # print('urllist',userlist)
        for projectend in Sql_projects:
            projectlist.append(str(projectend))
            # print"projectend",projectlist
        abc = len(userlist)
        print(abc)
        userlist.append(projectlist)
        print"end",userlist


        print("webuser-----",request.user.username)
        print("adf------",adf)
        if request.user.username in userlist and adf in userlist[abc]:
            print"userlist[0]",userlist
            print'userlost[abc]',userlist[abc]
            print("----success----")
            return True
        else:
            print("---fail--")
            print"userlist[0]",userlist
            print'userlost[abc]',userlist[abc]
            return False


def check_svnproject_permission(fun):
    def wapper(request, *args, **kwargs):
        if perm_svnproject_check(request, **kwargs):
            return fun(request, *args, **kwargs)
        return render(request, 'forbiden.html', locals())
    return wapper

