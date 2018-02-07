# -*- coding: utf-8 -*-
from django.conf.urls import url

from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetUserView, IndexView
from users.views import UploadImageView,ModifyPwdView,LogoutView,UserinfoView,UpdatePwdView,SendEmailCodeView
from users.views import UpdateEmailView,MyCourseView,MyFavOrgView,MyFavTeacherView,MyFavCourseView,MymessageView


urlpatterns =[
    #首页
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^register/$', RegisterView.as_view(), name='register'),

    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='user_active'),
    url(r'^forget/$', ForgetPwdView.as_view(), name='forget_pwd'),
    url(r'^reset/(?P<active_code>.*)/$', ResetUserView.as_view(), name='reset_pwd'),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name='modify_pwd'),
    url(r'^logout/$',LogoutView.as_view(),name='logout'),
    #用户信息
    url(r'^info/$',UserinfoView.as_view(),name='user_info'),
    #用户头像上传
    url(r'^image/upload/$',UploadImageView.as_view(),name='image_upload'),
    #用户中心修改密码
    url(r'^update/pwd/$',UpdatePwdView.as_view(),name='update_pwd'),
    #发送邮箱验证码
    url(r'^sendemail_code/$',SendEmailCodeView.as_view(),name='sendemail_code'),
    #修改邮箱
    url(r'^update_email/$',UpdateEmailView.as_view(),name='update_email'),
    #我的课程
    url(r'^mycourse/$',MyCourseView.as_view(),name='mycourse'),
    #我收藏的课程机构
    url(r'^myfav/org/$',MyFavOrgView.as_view(),name='myfav_org'),
    #我收藏的授课讲师
    url(r'^myfav/teacher/$',MyFavTeacherView.as_view(),name='myfav_teacher'),
    #我收藏的课程
    url(r'^myfav/course/$',MyFavCourseView.as_view(),name='myfav_course'),
    #我的消息
    url(r'^mymessage/$',MymessageView.as_view(),name='mymessage'),

]