# -*- coding：utf-8 -*-
__author__ = 'zhoujoe'
__date__ = '2019/11/26 22:47'


from django.conf.urls import url
from .views import CourseList, CourseDetail, CourseVedio, CourseComments, CourseAddComments, CourseVedioPlay


urlpatterns = [
    #课程列表页
    url(r'^list/$', CourseList.as_view(), name="course_list"),
    #课程详情页,因为需要知道是哪个课程，然后返回对应课程信息，这里url需要返回一个课程的id,
    #这个id会传到view视图类，以便找到这个课程的信息。
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetail.as_view(), name="course_detail"),
    url(r'^vedio/(?P<course_id>\d+)/$', CourseVedio.as_view(), name="course_vedio"),
    url(r'^comments/(?P<course_id>\d+)/$', CourseComments.as_view(), name="course_comments"),
    url(r'^add_comments/$', CourseAddComments.as_view(), name="add_comments"),
    url(r'^vedio_play/(?P<vedio_id>\d+)/$', CourseVedioPlay.as_view(), name="vedio_play"),
]