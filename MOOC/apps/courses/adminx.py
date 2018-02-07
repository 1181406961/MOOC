# -*- coding: utf-8 -*-
import xadmin
from .models import Course,Lesson,Video,CourseResource,BannerCourse
from organization.models import CourseOrg
class LessonInLine(object):
    model = Lesson
    extra = 0
class CourseResourceInline(object):
    model = CourseResource
    extra = 0
class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree','learn_times','students','get_zj_nums','go_to']
    search_fields = ['name', 'desc', 'detail', 'degree','learn_times','students','fav_nums','image','click_nums']
    list_filter = ['name', 'desc', 'detail', 'degree','learn_times','students','fav_nums','image','click_nums','add_time']
    #自定义排序
    ordering = ['-click_nums']
    #自定义只读
    readonly_fields = ['click_nums']
    #排除字段，与readonly冲突
    exclude =['fav_nums']
    #在列表页直接进行修改的功能
    list_editable =['degree','desc',]
    #添加course时添加lesson，只能嵌套一层
    inlines =[LessonInLine,CourseResourceInline]
    #定时刷新
    # refresh_times = [3,5]
    #设置detail的样式
    style_fields={'detail':'ueditor'}

    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    def save_models(self):
        #保存课程的时候统计课程机构的课程数
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()


class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree','learn_times','students','fav_nums','image','click_nums','add_time']
    search_fields = ['name', 'desc', 'detail', 'degree','learn_times','students','fav_nums','image','click_nums']
    list_filter = ['name', 'desc', 'detail', 'degree','learn_times','students','fav_nums','image','click_nums','add_time']
    #自定义排序
    ordering = ['-click_nums']
    #自定义只读
    readonly_fields = ['click_nums']
    #排除字段，与readonly冲突
    exclude =['fav_nums']
    #添加course时添加lesson，只能嵌套一层
    inlines =[LessonInLine,CourseResourceInline]
    #对列表的数据进行过滤
    def queryset(self):
        qs = super(BannerCourseAdmin,self).queryset()
        qs = qs.filter(is_banner=True)
        return qs

class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    #指定外键用来搜索的字段
    list_filter = ['course__name', 'name', 'add_time']

class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson__name', 'name', 'add_time']

class CourseResourceAdmin(object):
    list_display = ['course', 'name','download','add_time']
    search_fields = ['course', 'name','download']
    list_filter = ['course__name', 'name','download','add_time']

xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(BannerCourse,BannerCourseAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(CourseResource,CourseResourceAdmin)
