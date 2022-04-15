# -*- coding：utf-8 -*-
__author__ = 'zhoujoe'
__date__ = '2019/11/11 21:49'
from django import forms
import re

from operation.models import UserAsk

# 以前的方法
# class UserAskForm(forms.Form):
#     name = forms.CharField(required=True, min_length=2, max_length=50)
#     phone = forms.CharField(required=True, min_length=11, max_length=11)
#     course_name = forms.CharField(required=True, min_length=2, max_length=50)

# 新用的modelForm


class UserAskForm(forms.ModelForm):
    # 新增字段
    # my_filed = forms.CharField()

    class Meta:
        # 指明继承哪个类
        model = UserAsk
        # 指定继承哪些属性
        fields = ['name', 'mobile', 'course_name']

    # 二次清洗数据，函数必须以clean_开头，加上字段的名称作为函数名
    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号码非法", code="mobile_invalid")