# -*- coding: utf-8 -*-
from django.conf.urls import url

from users.views import LoginView,RegisterView,ActiveUserView,ForgetPwdView,ResetUserView,ModifyPwdView,LogoutView,UserinfoView




urlpatterns =[
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^register/$', RegisterView.as_view(), name='register'),

    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='user_active'),
    url(r'^forget/$', ForgetPwdView.as_view(), name='forget_pwd'),
    url(r'^reset/(?P<active_code>.*)/$', ResetUserView.as_view(), name='reset_pwd'),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name='modify_pwd'),
    url(r'^logout/$',LogoutView.as_view(),name='logout'),
    #用户信息
    url(r'^info/$',UserinfoView.as_view(),name='user_info'),
]