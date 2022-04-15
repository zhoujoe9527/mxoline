# -*- coding：utf-8 -*-
__author__ = 'zhoujoe'
__date__ = '2019/10/19 1:40'

import xadmin

from .models import CityDict, CourseOrg, Teacher


class CityDictAdmin(object):
    list_display = ('name', 'desc', 'add_time')
    search_fields = ('name', 'desc')
    # 显示外键的搜索
    list_filter = ('name', 'desc', 'add_time')


class CourseOrgAdmin(object):
    list_display = ('name', 'desc', 'click_nums', 'fav_nums', 'image', 'address', 'city', 'add_time')
    search_fields = ('name', 'desc', 'click_nums', 'fav_nums', 'image', 'address', 'city')
    list_filter = ('name', 'desc', 'click_nums', 'fav_nums', 'image', 'address', 'city', 'add_time')
    # 将下拉选择样式修改为输入关键字显示相关内容选择的样式
    relfield_style = 'fk-ajax'


class TeacherAdmin(object):
    list_display = ('org', 'name', 'work_year', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums', 'add_time')
    search_fields = ('org', 'name', 'work_year', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums')
    list_filter = ('org', 'name', 'work_year', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums', 'add_time')


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)


