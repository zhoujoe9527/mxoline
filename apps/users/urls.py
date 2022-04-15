# -*- coding：utf-8 -*-
__author__ = 'zhoujoe'
__date__ = '2020/5/18 15:39'

from django.conf.urls import url
from .views import UsersInfo, UserChangeAvatar, UpdatePwd, SendUpdateEmailCode, UpdateEmail, UserMyCourse
from .views import UserFavoriteCourse, UserFavoriteOrg, UserFavoriteTeacher, UserReadMessage

urlpatterns = [
    # 个人信息url
    url(r'^info/$', UsersInfo.as_view(), name="users_info"),

    # 修改头像
    url(r'^change_user_avatar/$', UserChangeAvatar.as_view(), name="change_user_avatar"),

    # 发送修改邮箱验证码
    url(r'^update_pwd/', UpdatePwd.as_view(), name="update_pwd"),

    # 发送修改邮箱验证码
    url(r'^update_email_code/', SendUpdateEmailCode.as_view(), name="update_email_code"),

    # 修改用户邮箱
    url(r'^update_email/', UpdateEmail.as_view(), name="update_email"),

    # 用户观看过的课程记录
    url(r'^my_course/', UserMyCourse.as_view(), name="my_course"),

    # 用户收藏课程
    url(r'^my_favorite/course/', UserFavoriteCourse.as_view(), name="my_favorite_course"),

    # 用户收藏教学机构
    url(r'^my_favorite/org/', UserFavoriteOrg.as_view(), name="my_favorite_org"),

    # 用户收藏授课教师
    url(r'^my_favorite/teacher/', UserFavoriteTeacher.as_view(), name="my_favorite_teacher"),

    # 用户消息
    url(r'^message/$', UserReadMessage.as_view(), name="user_message"),
]
