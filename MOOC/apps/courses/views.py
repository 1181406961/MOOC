# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from django.db.models import Q

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Course,CourseResource,Video
from operation.models import UserFavorite,CourseComment,UserCourse
from utils.mixin_utils import LoginRequiredMixin
# Create your views here.
class CourseListView(View):
    def get(self,request):
        all_courses = Course.objects.all().order_by('-add_time')
        #最热门，右边导航
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]
        search_keywords = request.GET.get('keywords','')
        #课程搜索
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords)|Q(detail__icontains=search_keywords))
        #排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_courses = all_courses.order_by('-students')
            elif sort == 'hot':
                all_courses = all_courses.order_by('-click_nums')
        # 对课程进行分页
        try:
            #将会在get请求中自动加上page参数
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        #params:per_page，每一页的数量(这里为3)
        p = Paginator(all_courses,3, request=request)

        courses = p.page(page)


        return render(request,'course-list.html',{
            'all_courses':courses,#这里传递的是Paginator对象
            'sort':sort,
            'hot_courses':hot_courses,

        })

class CourseDetailView(View):

    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        #增加点击数
        course.click_nums +=1
        course.save()
        #判断用户是否收藏课程和机构
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,fav_id=course.id,fav_type=1):#1表示课程
                has_fav_course =True
            if UserFavorite.objects.filter(user=request.user,fav_id=course.course_org.id,fav_type=2):#2表示机构
                has_fav_org =True
        #取出课程的关键字，进行相关性推荐
        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:1]
        else:
            #空的时候传一个数组，防报错
            relate_courses = []
        return render(request,'course-detail.html',{
            'course':course,
            'relate_courses':relate_courses,
            'has_fav_course':has_fav_course,
            'has_fav_org':has_fav_org,

        })

#使用多重继承时
# 1.如果每个类都有正确的写super(X, self).__init__()，那么mro顺序的所有的类的初始化方法都会执行一遍
#2.如果中途有的类没有写或错误的写了super(X, self).__init__()，
# 那么会按mro顺序执行到执行完没写的那个类， 执行结束。
class CourseInfoView(LoginRequiredMixin,View):
    #课程章节信息
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        course.students +=1
        course.save()
        #查询用户是否关联该课程
        user_courses = UserCourse.objects.filter(user=request.user,course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user,course=course)
            user_course.save()

        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [ user_courser.user.id for user_courser in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        #取出所有课程id
        course_ids =  [ user_courser.course.id for user_courser in all_user_courses]
        #获取学过该课程的用户还学过其他的课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]
        all_resources = CourseResource.objects.filter(course=course)
        return  render(request,'course-video.html',{
            'course':course,
            'all_resources':all_resources,
            'relate_courses':relate_courses,
        })

class CourseCommentView(LoginRequiredMixin,View):
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComment.objects.filter(course=course)
        return render(request, 'course-comment.html', {
            'course': course,
            'all_resources': all_resources,
            'all_comments':all_comments,
        })


class AddCommentsView(View):
    def post(self,request):
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')

        course_id = request.POST.get('course_id',0)
        comments = request.POST.get('comments','')
        if course_id >0 and comments:
            course = Course.objects.get(id=int(course_id))
            course_comments = CourseComment()
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success","msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"添加失败"}', content_type='application/json')

class VideoPlayView(View):
    #视频播放页面
    def get(self,request,video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        course.students += 1
        course.save()
        # 查询用户是否关联该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_courser.user.id for user_courser in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_courser.course.id for user_courser in all_user_courses]
        # 获取学过该课程的用户还学过其他的课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]
        all_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course-play.html', {
            'course': course,
            'all_resources': all_resources,
            'relate_courses': relate_courses,
            'video':video,
        })