# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Server(models.Model):
    # 服务器信息
    in_ip = models.CharField(max_length=255, null=True, blank=True, unique=True, verbose_name=u'内网IP')  # 内网ip
    ex_ip = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'外网IP')  # 弹性ip
    project_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'项目名称')
    host_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'主机名')
    position = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'位置')

    cpu_model = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'CPU型号')
    cpu_cores = models.IntegerField(null=True, blank=True, verbose_name=u'CPU核数')
    cpu_count = models.IntegerField(null=True, blank=True, verbose_name=u'CPU个数')

    mem = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'内存')
    disk = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'磁盘')
    os_version = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'系统版本')
    os_kernel = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'系统内核')
    status = models.NullBooleanField(default=False, null=True, blank=True, verbose_name=u'运行状态')
    max_open_files = models.IntegerField(null=True, blank=True, verbose_name=u'最大打开文件数')
    uptime = models.IntegerField(null=True, blank=True, verbose_name=u'在线时间（天）')

    def __unicode__(self):
        return '%s - %s' % (self.in_ip, self.host_name)


class Service(models.Model):
    '''
                服务
    '''
    server = models.ForeignKey(Server, verbose_name=u'服务器')
    port = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'端口')
    service_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'服务名')

    def __unicode__(self):
        return '%s - %s - %s' % (self.server.in_ip, self.port, self.service_name)