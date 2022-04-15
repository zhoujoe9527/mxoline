# -*- coding：utf-8 -*-
__author__ = 'zhoujoe'
__date__ = '2019/10/19 0:13'

from .models import Course, BannerCourse
from .models import Lesson
from .models import Video
from .models import CourseResource
import xadmin


# class LessonInline(object):
#     module = Lesson
#     extra = 0


class CourseAdmin(object):
    # 指定显示那些列
    list_display = ('name', 'desc', 'get_chapter_nums', 'is_banner', 'go_to', 'detail', 'degree', 'learn_times', 'student', 'fav_nums', 'image', 'click_nums', 'add_time')
    # 搜索
    # 时间搜索会报错，如何实现？
    search_fields = ('name', 'desc', 'detail', 'degree', 'learn_times', 'student', 'fav_nums', 'image', 'click_nums')
    # 筛选字段
    list_filter = ('name', 'desc', 'detail', 'degree', 'learn_times', 'student', 'fav_nums', 'image', 'click_nums', 'add_time')
    # 进入xadmin后，指定显示的内容的排序
    ordering = ['-click_nums']
    # 设置只读字段
    readonly_fields = ['click_nums', 'add_time']
    # 设置可见字段
    exclude = ['fav_nums']
    # 将字段设置为当前页面可编辑状态
    list_editable = ['is_banner', 'degree']
    # 设置刷新时间
    refresh_times = [30, 60]

    # 将下拉选择菜单修改为输入关键字显示相关选择的样式
    # 由于需要修改的‘课程机构’这个选项，它是一个外键，需要到课程机构的adminx中修改。

    # 课程中有章节，章节里面有视频，课程和章节的表是分开的，所以在xadmin中添加数据时，也是
    # 分开输入，这造成一定程度的麻烦，可以使用xadmin的line功能，可以使得在课程添加中出现章节的添加，
    # 但是由于是单继承，也就是说课程里面可以嵌套章节的信息，章节里面不能再嵌套视频信息。
    # inlines = [LessonInline, ] #有报错

    # 富文本编辑框
    style_fields = {'detail': 'ueditor'}

    def queryset(self):
        qs = super().queryset()
        qs = qs.filter(is_banner=False)
        return qs

    def save_models(self):
        # 在保存课程的同时统计课程机构的课程数
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org)
            course_org.save()


class BannerCourseAdmin(object):
    # 指定显示那些列
    list_display = ('name', 'desc', 'is_banner', 'detail', 'degree', 'learn_times', 'student', 'fav_nums', 'image', 'click_nums', 'add_time')
    # 搜索
    # 时间搜索会报错，如何实现？
    search_fields = ('name', 'desc', 'detail', 'degree', 'learn_times', 'student', 'fav_nums', 'image', 'click_nums')
    # 筛选字段
    list_filter = ('name', 'desc', 'detail', 'degree', 'learn_times', 'student', 'fav_nums', 'image', 'click_nums', 'add_time')
    # 进入xadmin后，指定显示的内容的排序
    ordering = ['-click_nums']
    # 设置只读字段
    readonly_fields = ['click_nums', 'add_time']
    # 设置可见字段
    exclude = ['fav_nums']

    def queryset(self):
        qs = super().queryset()
        qs = qs.filter(is_banner=True)
        return qs


class LessonAdmin(object):
    list_display = ('course', 'name', 'add_time')
    search_fields = ('course', 'name')
    # 显示外键的搜索
    list_filter = ('course__name', 'name', 'add_time')


class VideoAdmin(object):
    list_display =('lesson', 'name', 'add_time')
    search_fields = ('lesson', 'name')
    list_filter = ('lesson', 'name', 'add_time')


class CourseResourceAdmin(object):
    list_display = ('course', 'name', 'download', 'add_time')
    search_fields = ('course', 'name', 'download')
    list_filter = ('course', 'name', 'download', 'add_time')


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
