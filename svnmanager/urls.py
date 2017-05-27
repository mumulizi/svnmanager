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
from django.conf.urls import url,include
from django.contrib import admin
from app01 import views
from cronapp import urls as cron_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^$',views.index,name='index'),
    url(r'^$',views.showhost,name='showhost'),
    url(r'^login/$', views.login,name='login'),
    url(r'^logout/$',views.logout,name='logout'),
    url(r'^showsvn/$',views.showsvn,name='showsvn'),
    url(r'^svnadd/$',views.svnadd,name='addsvn'),
    url(r'^svnlog/$',views.showsvnlog,name='svnlog'),
    url(r'^svnedit/(?P<svn_id>[^/]+)$',views.svnedit,name='svnedit'),
    url(r'^group/$',views.group,name='group'),
    url(r'^addtogroup/$',views.addtogroup,name='addtogroup'),
    url(r'^onlinecode/$',views.onlinecode,name='onlinecode'),
    url(r'^svnupdate/(?P<svn_id>[^/]+)/(?P<u_type>[^/]+)$',views.svnupdate,name='svnupdate'),
    url(r'^pushonline/(?P<host_id>[^/]+)$',views.pushonline,name='pushonline'),
    url(r'^assets/$',views.assetslist,name='assets'),
    url(r'^cron/',include(cron_urls)),

]
