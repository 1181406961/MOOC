# -*- coding: utf-8 -*-
import json
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password

from pure_pagination import Paginator, PageNotAnInteger

from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm,UploadImageForm,UserInfoForm
from users.models import UserProfile, EmailVerifyRecord, Banner
from operation.models import UserCourse,UserFavorite,UserMessage
from organization.models import CourseOrg,Teacher
from courses.models import Course

from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin


class CustomBackend(ModelBackend):
    #重写authenticte方法
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # 使用get方法，因为get只能找一个。只希望找到一个user，当有两个user时就会抛出异常，
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        # form的参数是一个字典。POST是一个类字典结构，可以直接传入
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    next_html = request.META.get('HTTP_REFERER','')
                    # -1是没找到
                    if next_html.find('next') !=-1:
                        return redirect('%s'%next_html.split('=')[1])
                    return redirect(reverse('users:index'))
                else:
                    return render(request, 'login.html', {'msg': u'用户未激活！'})
            else:
                return render(request, 'login.html', {'msg': u'用户名密码错误！'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        context = {'register_form': register_form}
        return render(request, 'register.html', context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'login.html', {'msg': u'用户已经存在！', 'register_form': register_form})

            pass_word = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.password = make_password(pass_word)
            user_profile.is_active = False
            user_profile.save()
            send_register_email(user_name, 'register')
            #写入欢迎注册消息
            user_message = UserMessage()
            user_message.user=user_profile.id
            user_message.message = '欢迎注册MOOC'
            user_message.save()
            return redirect(reverse('users:login'))
        return render(request, 'register.html', {'register_form': register_form})


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
            return redirect(reverse('users:login'))
        else:
            return render(request, 'active_fail.html')


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email')
            send_register_email(email, 'forget')
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})
                # return redirect(reverse('login'))
        else:
            return render(request, 'active_fail.html')


class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'email': email, 'msg': u'密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return redirect(reverse('users:login'))
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email': email })

class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect(reverse('users:index'))


class UserinfoView(LoginRequiredMixin,View):
    #用户个人信息
    def get(self,request):
        return render(request,'usercenter-info.html')

    def post(self,request):
        user_info_form = UserInfoForm(request.POST,instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')

class UploadImageView(LoginRequiredMixin,View):
    #用户修改头像
    def post(self,request):
        #上传文件保存在FILES字段
        #instance指定一个实例
        image_form = UploadImageForm(request.POST,request.FILES,instance=request.user)
        if image_form.is_valid():
            # image = image_form.cleaned_data['image']
            # request.user.image = image
            # request.user.save()
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"添加出错"}', content_type='application/json')


class UpdatePwdView(View):
    #个人中心修改密码
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin,View):
    #发送邮箱验证码
    def get(self,request):
        email = request.GET.get('email','')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经存在"}', content_type='application/json')

        send_register_email(email, 'update_email')
        return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin,View):
    #修改个人邮箱
    def post(self,request):
        email = request.POST.get('email','')
        code = request.POST.get('code','')
        existed_records = EmailVerifyRecord.objects.filter(email=email,code=code,send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码出错"}', content_type='application/json')

class MyCourseView(LoginRequiredMixin,View):
    #我的课程
    def get(self,request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request,'usercenter-mycourse.html',{
            "user_courses":user_courses,
        })


class MyFavOrgView(LoginRequiredMixin,View):
    #我收藏的课程机构
    def get(self,request):

        fav_orgs = UserFavorite.objects.filter(user=request.user,fav_type=2,)
        org_list = [CourseOrg.objects.get(id=fav_org.fav_id) for fav_org in fav_orgs]
        return render(request,'usercenter-fav-org.html',{
            "org_list":org_list,
        })

class MyFavTeacherView(LoginRequiredMixin,View):
    #我收藏的授课讲师
    def get(self,request):

        fav_teachers = UserFavorite.objects.filter(user=request.user,fav_type=3,)
        teacher_list = [Teacher.objects.get(id=fav_teacher.fav_id) for fav_teacher in fav_teachers]
        return render(request,'usercenter-fav-teacher.html',{
            "teacher_list":teacher_list,
        })

class MyFavCourseView(LoginRequiredMixin,View):
    #我收藏的课程
    def get(self,request):

        fav_courses = UserFavorite.objects.filter(user=request.user,fav_type=1,)
        course_list = [Course.objects.get(id=fav_course.fav_id) for fav_course in fav_courses]
        return render(request,'usercenter-fav-course.html',{
            "course_list":course_list,
        })

class MymessageView(LoginRequiredMixin,View):
    #我的消息
    def get(self,request):
        all_message = UserMessage.objects.filter(user=request.user.id)
        # 课程机构分页
        try:
            # 将会在get请求中自动加上page参数
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # params:per_page，每一页的数量(这里为5)
        p = Paginator(all_message, 5, request=request)

        messages = p.page(page)
        return render(request,'usercenter-message.html',{
            'messages':messages,
        })

class IndexView(View):
    #首页
    def get(self,request):
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request,'index.html',{
            'all_banners':all_banners,
            'courses':courses,
            'banner_courses':banner_courses,
            'course_orgs':course_orgs
        })

def page_not_found(request):
    #全局处理404
    from django.shortcuts import render_to_response
    response = render_to_response('404.html',{})
    response.status_code =404
    return response

def page_error(request):
    #全局处理500
    from django.shortcuts import render_to_response
    response = render_to_response('500.html',{})
    response.status_code =500
    return response