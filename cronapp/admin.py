from django.contrib import admin

# Register your models here.
from cronapp import models

admin.site.register(models.cron_info)