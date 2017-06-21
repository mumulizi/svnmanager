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
from assets import  views
urlpatterns = [
    url(r'^server_list/$', views.index, name='index'),
    url(r'^server_add_page/$', views.server_add_page, name='server_add_page'),
    url(r'^server_add/$', views.server_add, name='server_add'),
    url(r'^server_edit_page/(?P<id>\d+)/$', views.server_edit_page, name='server_edit_page'),
    url(r'^server_edit/$', views.server_edit, name='server_edit'),
    url(r'^postmachineinfo/$', views.postmachineinfo , name='postmachineinfo'),
]
