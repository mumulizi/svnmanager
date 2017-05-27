#!/usr /bin/env python
#_*_ coding:utf-8_*_

from django.shortcuts import render,HttpResponse
from cronapp import  models
# Create your views here.
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
        post_cronname = request.POST.get('cronname')
        post_cronrule = request.POST.get('cronrule')
        post_cron_cmd = request.POST.get('cron_cmd')
        post_cron_service_ip = request.POST.get('cron_service_ip')
        post_crcrom_memo = request.POST.get('crom_memo')
        post_user = request.user.username
        print("cronmae:%s timerule:%s cron_cmd:%s serviceip:%s  memo:%s user:%s") %(post_cronname,post_cronrule,post_cron_cmd,
                                                                                    post_cron_service_ip,post_crcrom_memo,post_user)
        new_cron = models.cron_info(
            cron_name = post_cronname,
            cron_rule = post_cronrule,
            cron_cmd = post_cronrule,
            cron_service_ip = post_cron_service_ip,
            crom_memo = post_crcrom_memo,
            cron_owner = post_user
        )
        new_cron.save()
        cron_details = models.cron_info.objects.all()
        return render(request,'crontab/index.html',{'cron_details':cron_details})



def cron_edit(request,cron_id):
    get_post_cron_name = models.cron_info.objects.get(id=cron_id)

    # models.cron_info.objects.filter(id=cron_id).update('')

    return HttpResponse("aaaaaaa")

def cron_delete(request,cron_id):

    #删除前端提交的删除数据。获取id，根据id删除
    models.cron_info.objects.filter(id=cron_id).delete()
    cron_details = models.cron_info.objects.all()
    return render(request,'crontab/index.html',{'cron_details':cron_details})


def cron_stop(request,cron_id):
    # models.cron_info.objects.filter(id=cron_id)

    get_post_cron_name = models.cron_info.objects.get(id=cron_id)
    get_post_cron_status = get_post_cron_name.cron_status
    if get_post_cron_status =="running":
        models.cron_info.objects.filter(id=cron_id).update(cron_status='stop')
        cron_details = models.cron_info.objects.all()
        return render(request,'crontab/index.html',{'cron_details':cron_details})
    else:
        cron_details = models.cron_info.objects.all()
        return render(request,'crontab/index.html',{'cron_details':cron_details})

def cron_run(request,cron_id):
    get_post_cron_name = models.cron_info.objects.get(id=cron_id)
    get_post_cron_status = get_post_cron_name.cron_status
    if get_post_cron_status =="stop":
        models.cron_info.objects.filter(id=cron_id).update(cron_status='running')
        cron_details = models.cron_info.objects.all()
        return render(request,'crontab/index.html',{'cron_details':cron_details})
    else:

        cron_details = models.cron_info.objects.all()
        return render(request,'crontab/index.html',{'cron_details':cron_details})