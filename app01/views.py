# _*_ coding:utf-8 _*_
from django.shortcuts import render,HttpResponse,HttpResponseRedirect,render_to_response
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as user_login, logout as user_logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app01.app01form import *
from app01.app01function import *
from app01 import models
import string



def login(request):
    #登录功能

    if request.method == 'POST':
        #根据django自带的用户认证取出数据

        user = authenticate(username=request.POST.get('username'),
                            password=request.POST.get('password'))

        if user is not None:
            #使用自带认证登录
            user_login(request,user)
            #登录成功返回首页
            username = request.POST.get('username')
            return HttpResponseRedirect('/')
        else:
            #登录失败
            login_err = "Wrong username or password!"
            #返回错误消息
            return render(request, 'login.html', {'login_err':login_err})
    #如果是get
    return render(request, 'login.html')
#退出返回登录页
def logout(request):
    user_logout(request)
    return HttpResponseRedirect('/')


@login_required(login_url='/login/')
def showhost(request):
    if request.method == 'POST':
        search = request.POST.get("search",'null')
        print  request.POST,search
        qset = (
            Q(host_name__icontains = search) |
            Q(host_w_ip__icontains = search) |
            Q(host_w_port__icontains = search) |
            Q(host_n_ip__icontains = search) |
            Q(host_n_port__icontains = search) |
            Q(host_user__icontains = search)
            )
        host_list = models.hosts.objects.filter(qset)
        paginator = Paginator(host_list, 10)
        page = request.GET.get('page')
        try:
            host = paginator.page(page)
        except PageNotAnInteger:
            host = paginator.page(1)
        except EmptyPage:
            host = paginator.page(paginator.num_pages)
        host_group = models.hostgroup.objects.all()
        return render(request,'showhost.html',{'hosts':host,'hostgroups':host_group})
    else:
        host_list = models.hosts.objects.all()
        paginator = Paginator(host_list, 10)
        page = request.GET.get('page')
        try:
            host = paginator.page(page)
        except PageNotAnInteger:
            host = paginator.page(1)
        except EmptyPage:
            host = paginator.page(paginator.num_pages)
        host_group = models.hostgroup.objects.all()
        return render(request,'showhost.html',{'hosts':host,'hostgroups':host_group})




@login_required(login_url='/login/')
def showsvn(request):
    if request.method == "POST":
        search = request.POST.get("search",'null')
        qset = (
            Q(svn_name__icontains = search) |
            Q(svn_user__icontains = search) |
            Q(svn_local__icontains = search) |
            Q(svn_path__icontains = search) )
        svn_list = models.svns.objects.filter(qset)
        paginator = Paginator(svn_list, 10)
        page = 1
        try:
            svn = paginator.page(page)
        except PageNotAnInteger:
            svn = paginator.page(1)
        except EmptyPage:
            svn = paginator.page(paginator.num_pages)
        return render(request,'showsvn.html',{'svns':svn})
    else:
        svn_list = models.svns.objects.all()
        paginator = Paginator(svn_list, 10)
        page = request.GET.get('page')
        try:
            svn = paginator.page(page)
        except PageNotAnInteger:
            svn = paginator.page(1)
        except EmptyPage:
            svn = paginator.page(paginator.num_pages)
        return render(request,'showsvn.html',{'svns':svn})



@login_required(login_url='/login/')
def svnadd(request):
    # return HttpResponse("dadfadfsdfa")
    host123 = models.hosts.objects.all()
    if request.method == "POST":
        print("this is svnadd request======",request)
        svnname = request.POST.get('svnname')
        svnuser = request.POST.get('svnuser')
        svnpass = request.POST.get('svnpass')
        svnpasswd = en_str(svnpass)
        localpath = request.POST.get('localpath')
        svnpath = request.POST.get('svnpath')
        #host = request.POST.get('host')
        host = request.POST.get("host11_id")
        print("host======>::::",host)

        #print("=>:",svnname,svnuser,svnpass,localpath,svnpath,host)
        #print("=>:",svnname,svnuser,svnpass,localpath,svnpath)

        try:
            svns(svn_name=svnname,svn_user=svnuser,svn_pass=svnpasswd,svn_local=localpath,host_id = host,svn_path=svnpath,create_user=request.user).save()
        except:
             result = "Add Svn %s Failed!"%svnname
             return HttpResponse(result)





        # form = svnform(request.POST)
        # if form.is_valid():
        #     svn_name = form.cleaned_data['svn_name']
        #     svn_user = form.cleaned_data['svn_user']
        #     svn_pass = en_str(settings.SECRET_KEY,str(form.cleaned_data['svn_pass']))
        #     svn_local = form.cleaned_data['svn_local']
        #     svn_path = form.cleaned_data['svn_path']
        #     host = form.cleaned_data['host']
        #
        #     try:
        #         svns(svn_name=svn_name,svn_user=svn_user,svn_pass=svn_pass,svn_local=svn_local,svn_path=svn_path,host=host,create_user=request.user).save()
        #     except:
        #         result = "Add Svn %s Failed!"%svn_name
        #         form = svnform()
        #         return render(request,'addsvn.html',{'form':form,'result':result})
    return render(request,'addsvn.html',{'hostid11':host123})



@login_required(login_url='/login/')
def svnupdate(request,svn_id,u_type):
    svn = svns.objects.get(id =svn_id)
    host = svn.host
    u_type = u_type.encode('utf-8')
    if u_type == "1":
        cmd = r"svn update %s" %svn.svn_local
        print(cmd)
    elif u_type == "2":
        # version_cmd = r"svn info %s |grep Revision: |awk '{print $2}'" %svn.svn_local
        version_cmd = r"svn info %s | grep '^版本:' |awk {'print $2'}" %svn.svn_local
        try:
             now_version = ordinary_ssh(host=host.host_w_ip,username=host.host_user,password=host.host_pass,port=host.host_w_port,cmd=version_cmd)
        except:
            HttpResponse("get version fail！")
        print now_version
        restore_version = string.atoi(now_version)-1
        cmd = r"svn up -r %d  %s" %(restore_version,svn.svn_local)
    logname = time.strftime("%Y-%m-%d")+"-svn.log"
    svnlog = os.path.join(settings.BASE_DIR +'/'+ 'svnlog\\').replace('\\','/') +logname
    #svnlog = os.path.join(settings.BASE_DIR,'..\\','svnlog\\').replace('\\','/') +logname
    try:
        result = verification_ssh(host=host.host_w_ip,username=host.host_user,password=host.host_pass,port=host.host_w_port,root_pwd=host.host_root_pwd,cmd=cmd)
        print("res:"),result
    except Exception as e:
        return HttpResponse(str(e))
    if not os.path.exists(svnlog):
        f = open(svnlog,'a')
        f.close()
    out = open(svnlog,'a')
    svnname = svn.svn_name
    ss = '<br>'+str(time.strftime('%Y-%m-%d %H:%M'))+'<br>'
    print("webuser:----->",str(User.username))
    result = str(User.username)+ss + svnname.encode('utf-8') + ":<br>" +result.replace('\n','<br>')
    out.write(result.replace('<br>','\n')+'\n')
    out.write('\n-----------------------------------------------------------------\n')
    out.close()
    return render(request,'svnlog.html',{'result':result,'svnname':svnname})


@login_required(login_url='/login/')
def showsvnlog(request):
    logname = time.strftime("%Y-%m-%d")+"-svn.log"
    svnlog = os.path.join(settings.BASE_DIR +'/'+ 'svnlog\\').replace('\\','/') +logname
    print("svnlog--->",svnlog)
    try:
        f = open(svnlog)
        result = f.read()
        result = result.replace('\n','<br>')
    except Exception as e:
        return HttpResponse("读取日志失败！<br> %s" %str(e))
    f.close()
    return render(request,'svnlog.html',{'result':result})


#
# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         print("request is ---->:",request)
#         user = authenticate(username=username,password=password)
#         if user is not None:
#             if user.is_active:
#                 user_login(request,user)
#                 return render(request,'abc.html')
#             else:
#                 return HttpResponse("NO USER......")
#         else:
#             return HttpResponse("Passwd or User is Error...")
#     else:
#         return render(request,'login.html')
# def logout(request):
#     user_login(request)
#     return HttpResponseRedirect("/")


