# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.db.models import Q


from pure_pagination import Paginator, PageNotAnInteger

from .models import CourseOrg,CityDict,Teacher
from .forms import UserAskForm
from courses.models import Course
from operation.models import UserFavorite
class OrgView(View):
    #课程机构列表
    def get(self,request):
        #机构和城市
        all_orgs = CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by('-click_nums')[:3]
        all_citys = CityDict.objects.all()
        # 课程机构搜索
        search_keywords = request.GET.get('keywords','')
        if search_keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))
        #取出筛选城市
        city_id = request.GET.get('city','')
        if city_id:
            all_orgs =all_orgs.filter(city_id=int(city_id))
        #类别筛选
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)
        #根据学生人数和课程数量排序
        sort = request.GET.get('sort','')
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('-students')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('-course_nums')

        # 统计数量的函数
        org_nums = all_orgs.count()
        #课程机构分页
        try:
            #将会在get请求中自动加上page参数
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        #params:per_page，每一页的数量(这里为5)
        p = Paginator(all_orgs,5, request=request)

        orgs = p.page(page)

        return render(request,'org-list.html',{
            'all_orgs':orgs,
            'all_citys':all_citys,
            'org_nums':org_nums,
            'city_id':city_id,
            'category':category,
            'hot_orgs':hot_orgs,
            'sort':sort,

        })
        # 补充：<a href="?{{ page.querystring }}" </a>将自动把当前页面的query参数进行拼接



class AddUserAskView(View):
    def post(self,request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save()
            return HttpResponse('{"status":"success"}',content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"添加出错"}',content_type='application/json')

class OrgHomeView(View):
    #机构首页
    def get(self,request,org_id):
        current_page = "home"

        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()[:3]
        # 是否收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request,'org-detail-homepage.html',{
            'all_courses':all_courses,
            'all_teachers':all_teachers,
            'course_org':course_org,
            'current_page':current_page,
            'has_fav':has_fav,
        })

class OrgCourseView(View):
    #机构首页
    def get(self,request,org_id):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()
        # 是否收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request,'org-detail-course.html',{
            'all_courses':all_courses,
            'course_org':course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })
class OrgDescView(View):
    #机构详情页
    def get(self,request,org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 是否收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request,'org-detail-desc.html',{
            'course_org':course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgTeacherView(View):
    #机构教师页
    def get(self,request,org_id):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()
        # 是否收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request,'org-detail-teachers.html',{
            'all_teachers':all_teachers,
            'course_org':course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })

class AddFavView(View):
    #用户收藏,取消收藏
    def post(self,request):
        fav_id = request.POST.get('fav_id',0)
        fav_type = request.POST.get('fav_type',0)
        #匿名user也有is_authenticated,来判断是否登录
        if not request.user.is_authenticated() :

            return HttpResponse('{"status":"fail","msg":"用户未登录"}',content_type='application/json')

        exist_records = UserFavorite.objects.filter(user=request.user.id,fav_id=int(fav_id),fav_type=int(fav_type))
        if exist_records:
            #存在则取消
            exist_records.delete()
            return HttpResponse('{"status":"success","msg":"收藏"}', content_type='application/json')

        else:
            user_fav = UserFavorite()
            if int(fav_id) >0 and int(fav_type) >0:
                user_fav.fav_id  = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.user = request.user
                user_fav.save()
                return HttpResponse('{"status":"success","msg":"已收藏"}',content_type='application/json')
            else:
                return HttpResponse('{"status":"fail","msg":"收藏出错"}',content_type='application/json')



class TeacherListView(View):
    #课程讲师列表页
    def get(self,request):
        all_teachers = Teacher.objects.all()
        # 课程讲师搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_teachers = all_teachers.filter(Q(name__icontains=search_keywords) |
                                               Q(work_company__icontains=search_keywords)|
                                               Q(work_position__icontains=search_keywords))

        sort = request.GET.get('sort','')
        if sort and sort == 'hot':
            all_teachers = all_teachers.order_by('-click_nums')
        #右边讲师排行榜
        sorted_teacher = Teacher.objects.all().order_by('-click_nums')[:3]
        # 讲师分页
        try:
            # 将会在get请求中自动加上page参数
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # params:per_page，每一页的数量(这里为5)
        p = Paginator(all_teachers, 1, request=request)

        teachers = p.page(page)
        return render(request,'teachers-list.html',{
            'all_teachers':teachers,
            'sorted_teacher':sorted_teacher,
            'sort':sort,
        })


class TeacherDetailView(View):
    def get(self,request,teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        all_courses = Course.objects.filter(teacher=teacher)
        has_teacher_faved = False
        if UserFavorite.objects.filter(user=request.user,fav_type=3,fav_id=teacher.id):
            has_teacher_faved=True
        has_org_faved = False
        if UserFavorite.objects.filter(user=request.user,fav_type=2,fav_id=teacher.org.id):
            has_org_faved=True
        # 右边讲师排行榜
        sorted_teacher = Teacher.objects.all().order_by('-click_nums')[:3]

        return render(request,'teacher-detail.html',{
            'teacher':teacher,
            'all_courses':all_courses,
            'sorted_teacher': sorted_teacher,
            'has_teacher_faved':has_teacher_faved,
            'has_org_faved':has_org_faved,
        })
