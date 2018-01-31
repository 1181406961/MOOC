# -*- coding: utf-8 -*-
"""MOOC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
import xadmin
from django.views.generic import TemplateView
#处理静态文件的函数
from django.views.static import serve

from MOOC.settings import MEDIA_ROOT
urlpatterns = [
    #xadmin
    url(r'^xadmin/',xadmin.site.urls),
    #使用专门的模板类视图，来请求静态文件
    url(r'^$',TemplateView.as_view(template_name='index.html'),name='index'),
    #user相关
    url(r'users/',include('users.urls',namespace='users')),
    #验证码视图
    url(r'^captcha/', include('captcha.urls')),
    #课程机构url
    url(r'^org/', include('organization.urls',namespace='org')),
    #课程URL
    url(r'^course/', include('courses.urls',namespace='course')),

    #配置文件上传处理函数params：document_root：文件路径
    url(r'^media/(?P<path>.*)$',serve,{'document_root':MEDIA_ROOT})
]
