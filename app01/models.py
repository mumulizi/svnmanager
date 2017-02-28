# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
#多个svn对应一个host，外键应该在svn表里面
class hosts(models.Model):
    host_name = models.CharField(max_length=30)
    host_user = models.CharField(max_length=30)
    host_pass = models.CharField(max_length=50)
    host_w_ip = models.GenericIPAddressField()
    host_w_port = models.PositiveIntegerField()
    host_n_ip = models.GenericIPAddressField()
    host_n_port = models.PositiveIntegerField()
    host_root_pwd = models.CharField(max_length=50)
    script_dir = models.CharField(max_length=100)
    host_description = models.TextField(blank=True)
    create_user = models.CharField(max_length=10)

    def __unicode__(self):
        return self.host_name

class svns(models.Model):
    '''
            svn_local 是从svn下载的版本库的路径 就是在linux里把代码下载到了哪里 svn co svn://192.168.17.129.
            此处的例子是 /svadata/192.168.17.129的目录，不知道为啥是IP结尾的目录，反正下载下来就是这样，估计搭建SVN的时候没设置好
    '''
    svn_name = models.CharField(max_length=20)
    svn_user = models.CharField(max_length=30)
    svn_pass = models.CharField(max_length=30)
    svn_local = models.CharField(max_length=100)
    svn_path = models.CharField(max_length=100)
    host  = models.ForeignKey(hosts)
    create_user = models.CharField(max_length=10)
    def __unicode__(self):
        return self.svn_name


class hostgroup(models.Model):
    host_groupname = models.CharField(max_length=30)
    host = models.ManyToManyField(hosts)
    create_date = models.CharField(max_length=30)
    create_user = models.CharField(max_length=10)

    def __unicode__(self):
        return self.host_groupname

class scripts(models.Model):
    script_name = models.CharField(max_length=30)
    script_file = models.FileField(upload_to='aop/script/')
    script_date = models.CharField(max_length=50)
    script_description = models.TextField(blank=True)
    create_user = models.CharField(max_length=10)
    def __unicode__(self):
        return self.script_name

class scriptgroup(models.Model):
    script_groupname = models.CharField(max_length=30)
    script = models.ManyToManyField(scripts)
    create_date = models.CharField(max_length=30)
    create_user = models.CharField(max_length=10)
    def __unicode__(self):
        return self.script_groupname

class tasks(models.Model):
    task_name = models.CharField(max_length=50)
    script_group = models.ForeignKey(scriptgroup)
    host_group = models.ForeignKey(hostgroup)
    task_date = models.CharField(max_length=50)
    task_status = models.CharField(max_length=10)
    task_create_user = models.CharField(max_length=30)
    def __unicode__(self):
        return self.task_name

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(u"姓名",max_length=30)
    iphone = models.CharField(u'手机',max_length=11)