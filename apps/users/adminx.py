# -*- coding：utf-8 -*-
__author__ = 'zhoujoe'
__date__ = '2019/10/18 22:37'

import xadmin
from xadmin import views

from .models import EmailVerifyRecord, Banner, UserProfile
from courses.models import Course, Lesson, Video, CourseResource, BannerCourse
from operation.models import UserAsk, CourseComment, UserFavorite, UserMessage, UserCourse
from organization.models import CityDict, CourseOrg, Teacher


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = u"慕学后台管理体统"
    site_footer = u"慕学在线网"
    menu_style = "accordion"
    # global_search_models = [UserProfile, ]

    # 重新定义每个APP在xadmin中显示的位置和内容
    def get_site_menu(self):
        return (
            {'title': '课程管理', 'menus': (
                {'title': '课程信息', 'url': self.get_model_url(Course, 'changelist')},
                {'title': '轮播课程', 'url': self.get_model_url(BannerCourse, 'changelist')},
                {'title': '章节信息', 'url': self.get_model_url(Lesson, 'changelist')},
                {'title': '视频信息', 'url': self.get_model_url(Video, 'changelist')},
                {'title': '课程资源', 'url': self.get_model_url(CourseResource, 'changelist')},
            )},
            {'title': '机构管理', 'menus': (
                {'title': '所在城市', 'url': self.get_model_url(CityDict, 'changelist')},
                {'title': '机构讲师', 'url': self.get_model_url(Teacher, 'changelist')},
                {'title': '机构信息', 'url': self.get_model_url(CourseOrg, 'changelist')},
            )},
            {'title': '用户管理', 'menus': (
                {'title': '用户信息', 'url': self.get_model_url(UserProfile, 'changelist')},
                {'title': '邮箱验证', 'url': self.get_model_url(EmailVerifyRecord, 'changelist')},
                {'title': '首页轮播', 'url': self.get_model_url(Banner, 'changelist')},
            )},
            {'title': '用户操作', 'menus': (
                {'title': '用户咨询', 'url': self.get_model_url(UserAsk, 'changelist')},
                {'title': '用户课程', 'url': self.get_model_url(UserCourse, 'changelist')},
                {'title': '用户收藏', 'url': self.get_model_url(UserFavorite, 'changelist')},
                {'title': '用户消息', 'url': self.get_model_url(UserMessage, 'changelist')},
                {'title': '用户评论', 'url': self.get_model_url(CourseComment, 'changelist')}
            )},
        )


class EmailVerifyRecordAdmin(object):
    # 指定显示那些列
    list_display = ('code', 'email', 'send_type', 'send_time')
    # 搜索
    # 时间搜索会报错，如何实现？
    search_fields = ('code', 'email', 'send_type')
    # 筛选字段
    list_filter = ('code', 'email', 'send_type', 'send_time')
    model_icon = 'fa fa-user-circle-o'


class BannerAdmin(object):
    list_display = ('title', 'image', 'url', 'index', 'add_time')
    search_fields = ('title', 'image', 'url', 'index',)
    list_filter = ('title', 'image', 'url', 'index', 'add_time')
    model_icon = 'fa fa-user-circle-o'


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)

