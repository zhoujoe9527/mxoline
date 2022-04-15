# -*- coding：utf-8 -*-
__author__ = 'zhoujoe'
__date__ = '2019/10/23 21:26'

from captcha.fields import CaptchaField
from django import forms

from .models import UserProfile


# 将用户提交过来的表单做预处理，比如判断某个字段是否为空，长度。
class LoginForm(forms.Form):
    # required参数判断是否为空
    username = forms.CharField(required=True,
                               error_messages={"required": "用户名不能为空"} # 显示中文错误提示
                            )
    password = forms.CharField(required=True,
                               min_length=4,
                               error_messages={"required": "密码不能为空"}
                               )
    # 复习时需要实现的功能
    # 1.登录名和密码同时为空时，只提示一个框
    # 2.将提示框移动到头部位置
    # 3.将用户名，密码两个字用图标替换，在填写用户框内提示用户名，手机，邮箱，密码框内提示密码。
    # 钩子函数，自定义数据校验,对数据进行二次清洗，要更进一步验证数据，用这个方法。
    # 名称一定是clean_xxx,xxx为字段名，系统先调用clean_data,后调用clean_xxx。
    # def clean_password(self):
    #     user = self.cleaned_data.get("username")
    #     if user !=


class RegisterForm(forms.Form):
    # 每个Field会自动生成对应的html代码
    # 名字必须与html代码中的名字一致
    email_1 = forms.EmailField(required=True, error_messages={"required": "用户名不能为空"})
    # 需要实现输入两个密码并比较是否相等
    password = forms.CharField(required=True, min_length=5, error_messages={"required": u"密码不能为空"})
    captcha = CaptchaField(required=True, error_messages={"invalid": u"验证码错误"})


class ForgetPwdForm(forms.Form):
    email = forms.EmailField(required=True, error_messages={"required": "用户名不能为空"})
    # 需要实现输入两个密码并比较是否相等
    captcha = CaptchaField(required=True, error_messages={"invalid": u"验证码错误"})


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5, error_messages={"required": u"密码不能为空"})
    password2 = forms.CharField(required=True, min_length=5, error_messages={"required": u"密码不能为空"})


class ChangeUserAvatarForm(forms.ModelForm):
    class Meta:
        # 指明继承哪个类
        model = UserProfile
        # 指定继承哪些属性
        fields = ['image']


class UserInfoForm(forms.ModelForm):
    class Meta:
        # 指明继承哪个类
        model = UserProfile
        # 指定继承哪些属性
        fields = ['nick_name', 'birday', 'gender', 'address', 'mobile']
