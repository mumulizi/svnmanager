from django.contrib import admin

# Register your models here.
from app01 import models

admin.site.register(models.hosts)
admin.site.register(models.hostgroup)
admin.site.register(models.scriptgroup)
admin.site.register(models.scripts)
admin.site.register(models.svns)
admin.site.register(models.tasks)
admin.site.register(models.UserProfile)
