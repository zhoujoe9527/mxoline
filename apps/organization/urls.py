# -*- coding：utf-8 -*-
__author__ = 'zhoujoe'
__date__ = '2019/11/11 22:57'

from django.conf.urls import url
from .views import OrgView, AddUserAskView, OrgHomeView, OrgCourseView, OrgDescView, \
    OrgTeacherView, AddFavView, TeacherList, TeacherDetail

urlpatterns = [
    # 课程机构首页
    url(r'^list/$', OrgView.as_view(), name="org_list"),
    url(r'^add_ask', AddUserAskView.as_view(), name="add_ask"),
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="org_home"),
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name="org_course"),
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name="org_desc"),
    url(r'^teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name="org_teacher"),

    # 收藏
    url(r'^add_fav/$', AddFavView.as_view(), name="add_fav"),

    # 教师列表url
    url(r'^teacher/list/$', TeacherList.as_view(), name="teacher_list"),

    # 教师详情url
    url(r'^teacher/detail/(?P<teacher_id>\d+)/$', TeacherDetail.as_view(), name="teacher_detail"),
]