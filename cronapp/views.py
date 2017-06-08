#!/usr /bin/env python
#_*_ coding:utf-8_*_

from django.shortcuts import render,HttpResponse
from cronapp import  models
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import os,time
from django.contrib.auth import authenticate,login as user_login, logout as user_logout
from app01.views import login,logout,login_required
from cronapp.permission import check_cron_permission
# Create your views here.
@login_required(login_url='/login/')
def index(request):
    if request.method =='GET':

        cron_details = models.cron_info.objects.all()
        for cr_name in cron_details:
            cr_id = cr_name.id
            # cr_n = models.cron_info.objects.get(id=cr_id)
            rul = cr_name.cron_rule
            rcmd = cr_name.cron_cmd
            rip = cr_name.cron_service_ip
            rmemo = cr_name.crom_memo
            rown = cr_name.cron_owner
            print ("%s %s    %s   %s  %s  %s") %(cr_id,rul,rcmd,rip,rmemo,rown)
        return render(request,'crontab/index.html',{'cron_details':cron_details})
    else:
        post_cronname = str(request.POST.get('cronname'))
        post_cronrule = str(request.POST.get('cronrule'))
        post_cron_cmd = str(request.POST.get('cron_cmd'))
        post_cron_service_ip = request.POST.get('cron_service_ip')
        post_crcrom_memo = request.POST.get('crom_memo')
        post_run_user = str(request.POST.get('cron_run_user'))
        post_user = str(request.user.username)

        print("cronmae:%s timerule:%s cron_cmd:%s serviceip:%s  memo:%s run_user:%s user:%s") %(post_cronname,post_cronrule,post_cron_cmd,
                                                                                    post_cron_service_ip,post_crcrom_memo,post_run_user,post_user)
        new_cron = models.cron_info(
            cron_name = post_cronname,
            cron_rule = post_cronrule,
            cron_cmd = post_cron_cmd,
            cron_service_ip = post_cron_service_ip,
            crom_memo = post_crcrom_memo,
            cron_run_user = post_run_user,
            cron_owner = post_user
        )
        if post_run_user =='www':
            post_run_user='xiaogangtao'
        else:
            post_run_user=str(request.POST.get('cron_run_user'))
        cronfiletxt = post_cron_service_ip+"_"+post_run_user+"_"+"cronfile"
        add_cron_file = open(('./cronfile/%s')%(cronfiletxt),'a+')
        # os.system(("scp -P4591 root@%s:/var/spool/%s %s") %(post_run_user,post_run_user,post_cron_service_ip,cronfiletxt))
        add_cron = "#"+"    "+post_cronrule+"    "+post_cron_cmd + "\n"
        if add_cron in add_cron_file.readlines():
            return HttpResponse(u"已存在插入失败")
        else:
            new_cron.save()
            add_cron_file.write(add_cron)
            add_cron_file.close()
            cron_details = models.cron_info.objects.all()
            return render(request,'crontab/index.html',{'cron_details':cron_details})

@login_required(login_url='/login/')
@check_cron_permission
def cron_edit(request,cron_id):
    get_post_cron_name = models.cron_info.objects.get(id=cron_id)

    # models.cron_info.objects.filter(id=cron_id).update('')

    return HttpResponse("aaaaaaa")
@login_required(login_url='/login/')
@check_cron_permission
def cron_delete(request,cron_id):

    get_post_cron_name = models.cron_info.objects.get(id=cron_id)
    get_post_cron_status = get_post_cron_name.cron_status
    get_post_cron_rule  = str(get_post_cron_name.cron_rule)
    get_post_cron_cmd  = str(get_post_cron_name.cron_cmd)
    get_post_cron_ip = get_post_cron_name.cron_service_ip
    if get_post_cron_name.cron_run_user =="www":
        get_post_cron_run_user = "xiaogangtao"
    else:
        get_post_cron_run_user = get_post_cron_name.cron_run_user
    cronfiletxt = get_post_cron_ip+"_"+get_post_cron_run_user+"_"+"cronfile"
    web_cron = "#"+"    "+get_post_cron_rule+"    "+get_post_cron_cmd+"\n"
    web_cron_no_stop = get_post_cron_rule+"    "+get_post_cron_cmd+"\n"
    #删除前端提交的删除数据。获取id，根据id删除
    cronfile = open(('./cronfile/%s')%(cronfiletxt),'r+')          #一定不要用w+ 切记切记，用之前请百度他俩的区别
    cronfile_list = cronfile.readlines()
    models.cron_info.objects.filter(id=cron_id).delete()
    
    #算反射吧，不想写很多if else，想想就换个写法
    status = {"stop":web_cron,
              "running":web_cron_no_stop
              }
    if status.get(get_post_cron_status):
        ret_cron_index = cronfile_list.index(status.get(get_post_cron_status))
        print("need-delete-value:",cronfile_list[ret_cron_index])
        del cronfile_list[ret_cron_index]
        print("-delet--after--",cronfile_list)
        cronfile.seek(0)         #指针到开始0的位置
        cronfile.truncate()      #然后清空该文件 重新把列表写入进去
        for cron_data in cronfile_list:
            cronfile.write(cron_data)
        print(cronfile_list)
    cronfile.close()

    print ("cron_web_user:",request.user.username)
    # os.system("scp -P4591 %s xiaogangtao@%s:/var/spool/cron/%s"%(cronfiletxt,get_post_cron_ip,get_post_cron_run_user))
    os.system("sshpass -f /alidata/pangu/django/svnmanager/cronmanager/haha.py scp -P4591 ./cronfile/%s root@%s:/var/spool/cron/%s"%(cronfiletxt,get_post_cron_ip,get_post_cron_run_user))
    cron_details = models.cron_info.objects.all()
    return render(request,'crontab/index.html',{'cron_details':cron_details})
@login_required(login_url='/login/')
@check_cron_permission
def cron_stop(request,cron_id):
    # models.cron_info.objects.filter(id=cron_id)

    get_post_cron_name = models.cron_info.objects.get(id=cron_id)
    get_post_cron_status = get_post_cron_name.cron_status
    print("cron_web_user:%s run stop"%(request.user.username))
    if get_post_cron_status =="running":
        models.cron_info.objects.filter(id=cron_id).update(cron_status='stop')

        cron_details = models.cron_info.objects.all()
        return render(request,'crontab/index.html',{'cron_details':cron_details})
    else:
        cron_details = models.cron_info.objects.all()
        return render(request,'crontab/index.html',{'cron_details':cron_details})
@login_required(login_url='/login/')
@check_cron_permission
def cron_run(request,cron_id):
    get_post_cron_name = models.cron_info.objects.get(id=cron_id)
    get_post_cron_status = get_post_cron_name.cron_status
    get_post_cron_rule  = get_post_cron_name.cron_rule
    get_post_cron_cmd  = get_post_cron_name.cron_cmd
    print("cron_web_user:%s run cron_run")%(request.user.username)
    if get_post_cron_status =="stop":
        models.cron_info.objects.filter(id=cron_id).update(cron_status='running')

        #以下大段注释是因为添加了审核按钮，暂时不用点击stop或者start后就之间往文件内写了，写的操作转移到了 approval函数

        # cronfile = open('cronfile.txt','r+')          #一定不要用w+ 切记切记，用之前请百度他俩的区别
        # cronfile_list = cronfile.readlines()
        # web_cron = "#"+"    "+get_post_cron_rule+"    "+get_post_cron_cmd+"\n"
        # web_cron_no_stop = get_post_cron_rule+"    "+get_post_cron_cmd+"\n"
        # print("web_cron:",web_cron)
        # print("cronlist:",cronfile_list)
        # if web_cron in cronfile_list:
        #     ret_cron_index = cronfile_list.index(web_cron)
        #     print("need-delete-value----",cronfile_list[ret_cron_index])
        #     del cronfile_list[ret_cron_index]
        #     print("-delet--after--",cronfile_list)
        #     cronfile_list.insert(ret_cron_index,web_cron_no_stop)
        #     print("-insert-after---",cronfile_list)
        #     cronfile.seek(0)         #指针到开始0的位置
        #     cronfile.truncate()      #然后清空该文件 重新把列表写入进去
        #     for cron_data in cronfile_list:
        #         cronfile.write(cron_data)
        #     print(cronfile_list)
        #     cronfile.close()
        # elif web_cron_no_stop in cronfile_list:
        #     pass
        # else:
        #     cronfile_list.append(web_cron_no_stop)
        #     print"--new_add_cron--",web_cron_no_stop
        #     cronfile.seek(0)         #指针到开始0的位置
        #     cronfile.truncate()      #然后清空该文件 重新把列表写入进去
        #     for cron_nostop_data in cronfile_list:
        #         cronfile.write(cron_nostop_data)
        #     cronfile.close()
        #
        # print("-------sssscuess-------")
        # cronfile.close()
        cron_details = models.cron_info.objects.all()
        return render(request,'crontab/index.html',{'cron_details':cron_details})
    else:

        cron_details = models.cron_info.objects.all()
        return render(request,'crontab/index.html',{'cron_details':cron_details})

@login_required(login_url='/login/')
#审核按钮
@check_cron_permission
def approval(request):
    if request.method=="POST":
        check_box_list = request.POST.getlist('check_box_list')
        if check_box_list:
            print(check_box_list)
            cron_result = []

            for check_id in check_box_list:
                cron_id = str(check_id)
                get_post_cron_name = models.cron_info.objects.get(id=cron_id)
                get_post_cron_status = str(get_post_cron_name.cron_status)
                get_post_cron_rule  = str(get_post_cron_name.cron_rule)
                get_post_cron_cmd  = str(get_post_cron_name.cron_cmd)
                get_post_cron_ip = str(get_post_cron_name.cron_service_ip)
                if str(get_post_cron_name.cron_run_user) =="www":
                    get_post_cron_run_user = "xiaogangtao"
                else:
                    get_post_cron_run_user = str(get_post_cron_name.cron_run_user)
                cronfiletxt = get_post_cron_ip+"_"+get_post_cron_run_user+"_"+"cronfile"
                no_jing_ret = get_post_cron_rule + "    "+get_post_cron_cmd+"\n"
                ret = "#" + "    " +get_post_cron_rule + "    "+get_post_cron_cmd+"\n"

                cronfile = open(('./cronfile/%s')%(cronfiletxt),'r+')          #不要用w+ 切记切记，用之前请百度他俩的区别
                cronfile_list = cronfile.readlines()


                #如果前端提交的stop成立并且在计划任务里的该计划没有注释，那么就操作该if
                if get_post_cron_status =="stop" and no_jing_ret in cronfile_list:
                    print(cronfile_list)     #此print为了在log日志打印出来备份使用。万一计划任务清空，可根据该print找回
                    print("change:",ret)
                    cron_index = cronfile_list.index(no_jing_ret)
                    del cronfile_list[cron_index]
                    cronfile_list.insert(cron_index,ret)
                    cronfile.seek(0)         #指针到开始0的位置
                    cronfile.truncate()      #然后清空该文件 重新把列表写入进去
                    for cron_data in cronfile_list:
                        cronfile.write(cron_data)

                elif get_post_cron_status =="running"  and ret in cronfile_list:
                    print(cronfile_list)
                    print("change:",no_jing_ret)
                    cron_index = cronfile_list.index(ret)
                    del cronfile_list[cron_index]
                    cronfile_list.insert(cron_index,no_jing_ret)
                    cronfile.seek(0)         #指针到开始0的位置
                    cronfile.truncate()      #然后清空该文件 重新把列表写入进去
                    for cron_data in cronfile_list:
                        cronfile.write(cron_data)


                #如果页面存在计划任务 而服务器内不存在 则把存在的写入到服务器
                elif ret  not in cronfile_list and no_jing_ret not in cronfile_list:
                    print(ret,no_jing_ret)
                    print(cronfile_list)
                    if get_post_cron_status =="running":
                        cron_data = no_jing_ret
                    else:
                        cron_data = ret
                    cronfile_list.append(cron_data)
                    cronfile.seek(0)         #指针到开始0的位置
                    cronfile.truncate()      #然后清空该文件 重新把列表写入进去
                    for cron_data in cronfile_list:
                        cronfile.write(cron_data)

                cronfile.close()
                try:
                    #运行者只能使用xiaogangtao用户 和root用户 www用户好像没有key打通，而且xiaogangtao映射的www  /var/spool 下的名字也是xiaogangtao 和root
                    #可能会遇到权限问题，因为使用的是xiaogangtao用户运行的此系统，www目录的需要，可能就会对root计划任务无法操作  猜想的还没实验
                    new_file_name = get_post_cron_ip+"_"+get_post_cron_run_user+time.strftime("%Y%m%d%H%M%S", time.localtime()) 
                    src_ret = os.system(("sshpass -f /alidata/pangu/django/svnmanager/cronmanager/haha.py scp -P4591 root@%s:/var/spool/cron/%s /home/cronbak/%s")%(get_post_cron_ip,get_post_cron_run_user,new_file_name))
                    if src_ret==0:
                        os.system(("sshpass -f /alidata/pangu/django/svnmanager/cronmanager/haha.py scp -P4591 ./cronfile/%s root@%s:/var/spool/cron/%s")%(cronfiletxt,get_post_cron_ip,get_post_cron_run_user))
                        cron_result.append(u"执行成功"+get_post_cron_rule + get_post_cron_ip)
                    else:
                        print(u"源文件备份失败，以下不做操作")
                        cron_result.append(u"%s %s %s源文件备份失败，以下将不会做任何操作"%(get_post_cron_ip,get_post_cron_rule,get_post_cron_cmd))

                except:
                    print(u"计划任务拷贝过程失败")
                    cron_result.append(u"执行成功但传输失败"+"    "+get_post_cron_rule + "    "+get_post_cron_ip)
            return HttpResponse(cron_result)
        else:
            print("fail")
            return HttpResponse(u"未选择，请选择要执行的ID号")
@login_required(login_url='/login/')
@csrf_exempt
def getlog(request,cron_id):
    cron_id = str(cron_id)
    get_post_cron_name = models.cron_info.objects.get(id=cron_id)
    get_post_cron_ip =  get_post_cron_name.cron_service_ip
    # time_rule = get_post_cron_name.cron_rule
    # ret = str(get_post_cron_name)+"    "+ str(time_rule)+"."+"log"
    # return HttpResponse(ret)
    get_post_cron_cmd = get_post_cron_name.cron_cmd
    try:
        logfile = get_post_cron_cmd.split(">>")[1].split()[0]
        #print(get_post_cron_cmd)
        print(logfile)
        copy_ret = os.system(("sshpass -f /alidata/pangu/django/svnmanager/cronmanager/haha.py scp -P4591 root@%s:%s  ./cronlog/%s ")%(get_post_cron_ip,logfile,cron_id))
        if logfile == "/dev/null":
            return HttpResponse(u"/dev/null 是不可读取的日志，该计划任务未产生日志")
        else:
            copy_ret = os.system(("sshpass -f /alidata/pangu/django/svnmanager/cronmanager/haha.py scp -P4591 root@%s:%s  ./cronlog/%s ")%(get_post_cron_ip,logfile,cron_id))
            if copy_ret ==0:
                local_cronlog =open(("./cronlog/%s")%(cron_id),"r")
                local_log_file_read =local_cronlog.read()
                if local_log_file_read =='':
                    return HttpResponse(u"读取成功，但该计划任务未产生日志")
                else:
                    return HttpResponse(local_log_file_read)
            else:
                return HttpResponse(u"读取日志失败，联系管理员>")
    except IndexError:
        try:
            logfile = get_post_cron_cmd.split(">")[1].split()[0]
            print(logfile)
            if logfile == "/dev/null":
                return HttpResponse(u"/dev/null 是不可读取的日志，该计划任务未产生日志")
            else:
                copy_ret = os.system(("sshpass -f /alidata/pangu/django/svnmanager/cronmanager/haha.py scp -P4591 root@%s:%s  ./cronlog/%s ")%(get_post_cron_ip,logfile,cron_id))
                if copy_ret ==0:
                    local_log_file_read = open(("./cronlog/%s")%(cron_id),"r").read()
                    if local_log_file_read =='':
                        return HttpResponse(u"读取成功，但该计划任务未产生日志")
                    else:
                        return HttpResponse(local_log_file_read)
                else:
                    return HttpResponse(u"读取日志失败，联系管理员>")
        except IndexError:
            return HttpResponse(u"未检测到该命令有日志输出选项，请检查该计划任务的命令")



