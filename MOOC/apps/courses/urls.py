# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import  CourseListView,CourseDetailView,CourseInfoView,CourseCommentView,AddCommentsView,VideoPlayView
urlpatterns = [
    #课程列表
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
    #课程详情
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),

    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='course_info'),
    #显示课程评论
    url(r'^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name='course_comments'),
    #添加课程评论
    url(r'^add_comment/$', AddCommentsView.as_view(), name='add_comment'),
    #
    url(r'^video/(?P<video_id>\d+)/$', VideoPlayView.as_view(), name='video_play'),

]