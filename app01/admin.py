from django.contrib import admin

# Register your models here.
from app01 import models

admin.site.register(models.hosts)
admin.site.register(models.hostgroup)
#admin.site.register(models.scriptgroup)
#admin.site.register(models.scripts)
admin.site.register(models.svns)
#admin.site.register(models.tasks)
#admin.site.register(models.online)
admin.site.register(models.cmdb)
admin.site.register(models.svn_permission)
admin.site.register(models.online_permission)
#admin.site.register(models.UserProfile)
admin.site.register(models.Permission)

class onlineadmin(admin.ModelAdmin):
    list_display = ("shost",'sdir','sexcludedir')
admin.site.register(models.online,onlineadmin)

