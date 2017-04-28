# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
#多个svn对应一个host，外键应该在svn表里面
class hosts(models.Model):
    host_name = models.CharField(max_length=30)
    host_user = models.CharField(max_length=30)
    host_pass = models.CharField(max_length=50,blank=True,null=True)
    host_w_ip = models.GenericIPAddressField()
    host_w_port = models.PositiveIntegerField()
    host_n_ip = models.GenericIPAddressField()
    host_n_port = models.PositiveIntegerField()
    host_root_pwd = models.CharField(max_length=50,blank=True,null=True)
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

class online(models.Model):
    shost = models.GenericIPAddressField(u'预发布机',max_length=100)
    sdir = models.CharField(max_length=100)
    sexcludedir = models.CharField(max_length=100,blank=True,null=True)
    dhost = models.ManyToManyField(hosts)
    ddir = models.CharField(max_length=100)
    def __unicode__(self):
        return self.shost

class cmdb(models.Model):
    AssetType = models.CharField(u'资产类型',max_length=100)
    AssetSn = models.CharField(u'资产编号',max_length=50)
    # ServerName = models.ManyToManyField(hosts)
    ServerName = models.CharField(u'资产名',max_length=100)
    IP = models.GenericIPAddressField(u'IP地址',max_length=50,blank=True,null=True)
    MAC = models.CharField(u'MAC地址',max_length=50,blank=True,null=True)
    ServerType = models.CharField(u'资产型号',max_length=50)
    ServerSN = models.CharField(u'资产SN',max_length=50)
    Disk = models.CharField(u'硬盘',max_length=50,blank=True,null=True)
    DiskSN = models.CharField(u'硬盘序列号',max_length=50,blank=True,null=True)
    RaidInfo = models.CharField(u'Raid信息',max_length=100,blank=True,null=True)
    Mem = models.CharField(u'内存',max_length=50,blank=True,null=True)
    CPU = models.CharField(max_length=100,blank=True,null=True)
    iDracIP = models.GenericIPAddressField(u'管理IP',max_length=50,blank=True,null=True)
    Memo = models.CharField(u'备注',max_length=200,blank=True,null=True)

    def __unicode__(self):
        return self.ServerName



class Permission(models.Model):
    name = models.CharField("权限名称", max_length=64)
    url = models.CharField('URL名称', max_length=255)
    chioces = ((1, 'GET'), (2, 'POST'))
    per_method = models.SmallIntegerField('请求方法', choices=chioces, default=1)
    argument_list = models.CharField('参数列表', max_length=255, help_text='多个参数之间用英文半角逗号隔开', blank=True, null=True)
    describe = models.CharField('描述', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '页面权限表'
        verbose_name_plural = verbose_name
        #权限信息，这里定义的权限的名字，后面是描述信息，描述信息是在django admin中显示权限用的
        permissions = (
            ('views_svns_list', '查看svn版本库信息表'),
            ('views_onlinecode_info', '查看推送代码详细信息表'),
            ('views_assets_info', '查看资产详细信息表'),
        )





class svn_permission(models.Model):
    permission_info = models.CharField(max_length=100)
    web_users = models.ManyToManyField(User)
    svn_projects = models.ManyToManyField(svns)
    def __unicode__(self):
        return self.permission_info
    class Meta:
        verbose_name = 'SVN权限表'
        verbose_name_plural = verbose_name

class online_permission(models.Model):
    permission_info = models.CharField(max_length=100,blank=True,null=True)
    web_users = models.CharField(max_length=100)
    src_dir = models.TextField()

    def __unicode__(self):
        return self.permission_info
    class Meta:
        verbose_name = '上线代码权限表'
        verbose_name_plural = verbose_name
