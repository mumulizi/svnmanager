#!/usr/bin/env python
#_*_coding:utf-8_*_
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class cron_info(models.Model):
    cron_name = models.CharField(u'任务名',max_length=100)
    status_choices = (
                      ('stop',u'禁用'),
                      ('running',u'启用')
                    )
    cron_status = models.CharField(u'状态',choices=status_choices,default='stop',max_length=32) #0 禁用  1 启用
    cron_rule = models.CharField(max_length=50,verbose_name="时间规则")
    cron_cmd = models.CharField(max_length=512,verbose_name="命令")
    cron_service_ip = models.GenericIPAddressField(u'运行的服务器IP')
    crom_memo = models.CharField(max_length=200,verbose_name="功能备注",blank=True,null=True)
    #action_choices = (
    #                   ('edit',u'编辑')
    #                   ('delete',u'删除')
    #                   ('run',u'启用')
    #                   ('stop',u'禁止')
    #                 )
    #cron_action = models.CharField(u'操作',choices = action_choices,default='stop',max_length=128)
    cron_owner = models.CharField(u'创建人',max_length=150)
    cron_run_user = models.CharField(u'运行者',max_length=20)
    #cron_logfile =

    def __str__(self):
        return self.cron_name
    class Meta:
        verbose_name = '任务管理'
        verbose_name_plural = "任务管理"
        index_together = ('cron_status','cron_rule','cron_cmd','cron_service_ip')
        unique_together=[
            ('cron_status','cron_rule','cron_cmd','cron_service_ip')
        ]
