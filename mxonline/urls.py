"""mxonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.views.generic import TemplateView
from extra_apps import xadmin
from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetView, ModifyPwdView
from users.views import LogoutView, Index
#处理静态文件
from django.views.static import serve

from .settings import MEDIA_ROOT
#from .settings import STATIC_ROOT


urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url('^$', Index.as_view(), name="index"),
    url('^login/$', LoginView.as_view(), name="login"),
    url('^logout/$', LogoutView.as_view(), name="logout"),
    url('^register', RegisterView.as_view(), name='register'),
    #引入了其它的url.py文件，所有已captcha开头的url都会交给'captcha.urls'来处理
    #后面需要实现，给个APP需要用自己的urls.py文件。
    url(r'^captcha/', include('captcha.urls')),
    #?p提取一个自己命名为active_code的变量
    url(r'active/(?P<active_code>\w+)/$', ActiveUserView.as_view(), name="user_active"),
    url(r'^forgetpwd/$', ForgetPwdView.as_view(), name="forget_pwd"),
    url(r'^reset/(?P<reset_code>\w+)/$', ResetView.as_view(), name="reset_pwd"),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name="modify_pwd"),

    #课程机构url配置
    url(r'^org/', include(('organization.urls', 'organization'), namespace="org")),

    #配置上传文件的访问处理函数，例如通过url显示图片
    url(r'^media/(?P<path>.*$)', serve, {"document_root": MEDIA_ROOT}),

    #公开课程url配置
    url(r'^course/', include(('courses.urls', 'courses'), namespace="course")),

    #教师url配置
    url(r'^teacher/', include(('organization.urls', 'organization'), namespace="teacher")),

    #个人信息中心url配置
    url(r'^users/', include(('users.urls', 'users'), namespace="users")),


    # 配置静态访问文件的的处理
    # url(r'^static/(?P<path>.*$)', serve, {"document_root": STATIC_ROOT}),

    # 富文本编辑器
    url(r'^ueditor/', include('DjangoUeditor.urls')),

]

# 配置全局404和500错误页面
