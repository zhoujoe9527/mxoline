from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.db.models import Q

from .models import Course, CourseResource, Video
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from operation.models import UserFavorite
from operation.models import UserCourse, CourseComment
from utils.mixin_utils import LoginRequiredMixin


class CourseList(View):
    # 课程列表页
    def get(self, request):

        # 获取数据库course表所有的数据，通过querySet API获取
        all_course = Course.objects.all().order_by("-add_time")

        # 热门课程推荐,
        hot_courses = Course.objects.all().order_by("-click_nums")[:3]

        # 课程搜索, name__icontains：这个关键字可以拆分为四个部分，name表示的course表的name字段，
        # 双下滑线表示对这个字段做某种操作，i表示不区分大小写，contains表示做like查询
        # 整句的意思就是对传回来的关键字，生成select语句，用like来查询。
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_course = all_course.filter(Q(name__icontains=search_keywords) |\
                                           Q(desc__icontains=search_keywords) |\
                                           Q(detail__icontains=search_keywords))

        # 筛选。通过html sort返回的筛选的类型的值，根据类型进行排序。
        sort_mode = request.GET.get('sort', "")
        if sort_mode == 'student':
            all_course = all_course.order_by('-students')
        elif sort_mode == 'hot':
            all_course = all_course.order_by('-click_nums')

        # 对课程列表进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_course, 3, request=request)
        # 分页数据, 是一个Paginator对象, 需要遍历时,要用到objects_list属性,courses.object_list
        courses = p.page(page)

        return render(request, 'course-list.html', {
            "all_course": courses,
            "sort_mode": sort_mode,
            "hot_courses": hot_courses
        })


class CourseDetail(View):
    """
    课程详情页
    """
    def get(self, request, course_id):

        course = Course.objects.get(id=int(course_id))
        # 记录课程点击数
        course.click_nums += 1
        course.save()

        # 收藏功能
        has_fav_org = False
        has_fav_course = False

        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True
        # 课程推荐
        tag = course.tag
        if tag:
            relative_courses = Course.objects.filter(tag = tag)[:2]
        else:
            relative_courses = []

        return render(request, 'course-detail.html', {
            "course": course,
            "relative_courses": relative_courses,
            "has_fav_course": has_fav_course,
            "has_fav_org": has_fav_org
        })


class CourseVedio(LoginRequiredMixin, View):
    """
    章节信息，这里需要继承一个基础的视图类LoginRequiredMixin，该类的
    作用是在进入视图类之前做登录验证。放在utils下的mixin中
    """

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 用户学生数加1
        course.student += 1
        course.save()

        # 课程资源
        course_resource = CourseResource.objects.filter(course_id=course_id)

        # 查询用户是否已经关联了课程
        user_is_relate_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_is_relate_course:
            user_this_course = UserCourse(user=request.user, course=course)
            user_this_course.save()

        # 在用户课程表中找到选择了这门课程的所有的记录
        user_courses = UserCourse.objects.filter(course=course)

        # 获取学过这门课程的所有学生
        user_ids = [user_course.user.id for user_course in user_courses]
        
        # UserCourse表中，user是一个外键，可以通过_下划线获取user表中的字段,这样就可以使用
        # id来查询，而不用传递user对象了。
        # 可以在查询的字段名称后面加两个下划线和in，表名后面的参数是一个list.
        this_course_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有的课程id
        all_coourse_ids = [user_course.course.id for user_course in this_course_user_courses]
        # 由于学生学习的课程可能重复，这里将重复的课程ID去除，同时将本课程的ID去除，保留其它课程的ID。
        # remove函数对列表本身修改，没有返回值。
        other_course_ids = list(set(all_coourse_ids))
        other_course_ids.remove(int(course_id))
        # 取出学过该课程的学生学过的所有课程,取前五个
        user_other_courses = Course.objects.filter(id__in=other_course_ids).order_by('-click_nums')[:5]

        # 该课程的同学还学过的其它课程
        # course_users = course.usercourse_set.all()
        # all_user_courses = UserCourse.objects.all()
        # other_courses_user = []
        # exist_course_list = []
        # for course_user in course_users:
        #     for user_course in all_user_courses:
        #        if course_user.user_id == user_course.user_id and user_course.course_id != int(course_id) and user_course.course_id not in exist_course_list:
        #             exist_course_list.append(user_course.course_id)
        #             other_courses_user.append(user_course)

        return render(request, 'course-video.html', {
            'course': course,
            'course_resource': course_resource,
            'user_other_courses': user_other_courses
        })


class CourseComments(LoginRequiredMixin, View):
    """
    用户评论视图类
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id.strip()))
        all_user_course_comment = CourseComment.objects.filter(course=course).order_by('-add_time')
        course_resource = CourseResource.objects.filter(course_id=course_id)

        return render(request, "course-comment.html", {
            'course': course,
            'all_user_course_comment': all_user_course_comment,
            'course_resource': course_resource
        })


class CourseAddComments(LoginRequiredMixin, View):

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')
        if int(course_id) > 0 and comments:
            user_course_comment = CourseComment()
            user_course_comment.user = request.user
            user_course_comment.course = Course.objects.get(id=int(course_id))
            user_course_comment.comments = comments
            user_course_comment.save()
            return HttpResponse('{"status":"success", "msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加失败"}', content_type='application/json')


class CourseVedioPlay(LoginRequiredMixin, View):
    def get(self, request, vedio_id):
        vedio = Video.objects.get(id=int(vedio_id))

        course = Course.objects.get(id=vedio.lesson.course.id)
        course_id = course.id

        course_resource = CourseResource.objects.filter(course_id=course_id)

        # 查询用户是否已经关联了课程
        user_is_relate_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_is_relate_course:
            user_this_course = UserCourse(user=request.user, course=course)
            user_this_course.save()

        # 在用户课程表中找到选择了这门课程的所有的记录
        user_courses = UserCourse.objects.filter(course=course)

        # 获取学过这门课程的所有学生
        user_ids = [user_course.user.id for user_course in user_courses]

        # UserCourse表中，user是一个外键，可以通过_下划线获取user表中的字段,这样就可以使用
        # id来查询，而不用传递user对象了。
        # 可以在查询的字段名称后面加两个下划线和in，表名后面的参数是一个list.
        this_course_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有的课程id
        all_coourse_ids = [user_course.course.id for user_course in this_course_user_courses]
        # 由于学生学习的课程可能重复，这里将重复的课程ID去除，同时将本课程的ID去除，保留其它课程的ID。
        # remove函数对列表本身修改，没有返回值。
        other_course_ids = list(set(all_coourse_ids))
        other_course_ids.remove(int(course_id))
        # 取出学过该课程的学生学过的所有课程,取前五个
        user_other_courses = Course.objects.filter(id__in=other_course_ids).order_by('-click_nums')[:5]

        return render(request, 'course-play.html', {
            'vedio': vedio,
            'course': course,
            'course_resource': course_resource,
            'user_other_courses': user_other_courses
        })