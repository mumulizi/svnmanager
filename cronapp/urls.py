"""svnmanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from cronapp import views


urlpatterns = [
    url(r'^$',views.index,name='cronindex'),
    # url(r'^addcron/$',views.addcron,name='addcron'),
    url(r'^edit/(?P<cron_id>[^/]+)$',views.cron_edit,name='cron_edit'),
    url(r'^delete/(?P<cron_id>[^/]+)$',views.cron_delete,name='cron_delete'),
    url(r'^stop/(?P<cron_id>[^/]+)$',views.cron_stop,name='cron_stop'),
    url(r'^run/(?P<cron_id>[^/]+)$',views.cron_run,name='cron_run'),
]
