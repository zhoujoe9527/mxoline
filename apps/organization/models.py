# -*- encoding:utf-8 -*-
from django.db import models
from datetime import datetime
# Create your models here.


class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name=u"城市名")
    desc = models.CharField(max_length=200, verbose_name=u"描述")
    add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"城市"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"机构名称")
    desc = models.TextField(verbose_name=u"机构描述")
    tag = models.TextField(max_length=10, default="", verbose_name="机构头衔")
    category = models.CharField(default="pxjg", max_length=20, choices=(("pxjg", "培训机构"), ("gr", "个人"), ("gx", "高校")), verbose_name=u"机构类别")
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏数")
    image = models.ImageField(upload_to="org/%Y/%m", verbose_name=u"封面图")
    address = models.CharField(max_length=150, verbose_name=u"机构地址")
    city = models.ForeignKey(CityDict, verbose_name=u"所在城市", on_delete=models.CASCADE)
    add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    course_nums = models.IntegerField(default=0, verbose_name=u"课程数")

    def get_teacher_nums(self):
        # 获取课程机构的教师数量
        return self.teacher_set.all().count()

    def get_course_nums(self):
        # 获取教学机构的课程数
        return self.course_set.all().count()

    class Meta:
        verbose_name = u"课程机构"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, verbose_name=u"所属机构", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name=u"教师名")
    work_year = models.IntegerField(default=0, verbose_name=u"工作年限")
    work_company = models.CharField(max_length=100, verbose_name=u"就职公司")
    work_position = models.CharField(max_length=50, verbose_name=u"公司职位")
    points = models.CharField(max_length=50, verbose_name=u"教学特点")
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏数")
    image = models.ImageField(default='', upload_to="teacher/%Y/%m", verbose_name=u"头像")
    age = models.CharField(max_length=10, verbose_name=u"教师年龄", default="未知")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"教师"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    # 不建议这种写法，应该在view中写一个函数，model只写数据库字段，不把数据库数据和逻辑混在一起，
    # 这样代码结构更加清晰，可读性更好
    # 获取教师的课程数量
    # def get_teacher_course_num(self):
    #     return self.course_set.all().count()
