# -*- encoding:utf-8 -*-
from django.db import models
from datetime import datetime
# Create your models here.

from organization.models import CourseOrg, Teacher
from DjangoUeditor.models import UEditorField


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name=u"课程机构", on_delete=models.CASCADE, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, verbose_name=u"课程老师", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u"课程名")
    desc = models.CharField(max_length=300, verbose_name=u"课程描述")
    is_banner = models.BooleanField(default=False, verbose_name="是否轮播")
    # TextField长度没有限制
    detail = UEditorField(width=600, height=300, verbose_name=u"课程详情", imagePath='courses/ueditor/',
                          default='')
    degree = models.CharField(verbose_name=u"难度", choices=(("cj", "初级"), ("zj", "中级"), ("gj", "高级")), max_length=2)
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长(分钟数)")
    student = models.IntegerField(default=0, verbose_name=u"学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name=u"封面图", max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    category = models.CharField(max_length=20, verbose_name=u"课程类别", default='')
    tag = models.CharField(max_length=10, verbose_name=u"课程标签", default='')
    course_knowledge = models.CharField(max_length=100, verbose_name=u"课程需知", default='')
    course_target = models.CharField(max_length=120, verbose_name=u"课程目标", default='')
    add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")

    def get_chapter_nums(self):
        # 通过外键，反向查找leason
        return self.lesson_set.all().count()
    get_chapter_nums.short_description = u'章节数'

    # 在xadmin中设置一个跳转
    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<a href='http://www.baidu.com'>跳转</a>")
    go_to.short_description = u'跳转'

    def get_learn_users(self):
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):
        return self.lesson_set.all()

    # def get_course_resource(self):
    #     """
    #     course中的数据和courseResource表中的数据是一对多的关系。
    #     courseResource表的course字段是外键，可以在course表中反向获取courseResource表的信息
    #     同时建议不要在models中使用这种方法获取其它表的信息，应该在views函数中实现。
    #     :return:
    #     """
    #     return self.courseresource_set.all()

    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class BannerCourse(Course):
    class Meta:
        verbose_name = u'轮播课程'
        verbose_name_plural = verbose_name
        # proxy为False时，会生成BannerCourse,Course两张表，为True时，只有一张表，都是Course表
        proxy = True


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=u"章节名")
    add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_vedios(self):
        return self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u"章节", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=u"视频名")
    vedio_url = models.CharField(max_length=100, verbose_name=u"视频链接", default="", null=True,  blank=True)
    vedio_time = models.IntegerField(default=0, verbose_name=u"视频时长(分钟数)", null=True, blank=True)
    add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_format_time(self):
        seconds = self.vedio_time*60
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        if h > 0:
            return "%d:%02d:%02d" % (h, m, s)
        else:
            return "%02d:%02d" % (m, s)


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=u"名称")
    download = models.FileField(upload_to="course/resource/%Y/%m", verbose_name=u"资源文件", max_length=100)
    add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程资源"
        verbose_name_plural = verbose_name


