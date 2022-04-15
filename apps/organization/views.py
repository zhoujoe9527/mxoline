from django.shortcuts import render
# Create your views here.
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q

from .models import CourseOrg, CityDict, Teacher
from courses.models import Course
from .forms import UserAskForm
from courses.models import Course
from operation.models import UserFavorite
from utils.PaginatorUtils import PaginatorUtils

class OrgView(View):
    """
    课程机构列表功能
    """
    def get(self, request):
        # 课程机构
        all_orgs = CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by('-click_nums')[:3]
        # 城市
        all_citys = CityDict.objects.all()

        # 课程搜索, name__icontains：这个关键字可以拆分为四个部分，name表示的course表的name字段，
        # 双下滑线表示对这个字段做某种操作，i表示不区分大小写，contains表示做like查询
        # 整句的意思就是对传回来的关键字，生成select语句，用like来查询。
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) |\
                                       Q(desc__icontains=search_keywords) |\
                                       Q(address__icontains=search_keywords))

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 取出筛选城市
        city_id = request.GET.get('city', "")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 类别筛选
        category = request.GET.get('ct', "")
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 排序
        # 目前只是降序显示，后续要实现升序，降序排列显示。
        sort_mode = request.GET.get('sort', "")
        if sort_mode == 'students':
            all_orgs = all_orgs.order_by('-students')
        elif sort_mode == 'courses':
            all_orgs = all_orgs.order_by('-course_nums')

        org_nums = all_orgs.count()
        # Provide Paginator with the request object for complete querystring generation
        # 分页，将全部机构每页5个显示
        p = Paginator(all_orgs, 5, request=request)

        orgs = p.page(page)

        return render(request, 'org-list.html', {
            "all_orgs": orgs,
            "all_citys": all_citys,
            "org_nums": org_nums,
            "city_id": city_id,
            "category": category,
            "hot_orgs": hot_orgs,
            "sort_mode": sort_mode
        })


class AddUserAskView(View):
    """
    用户添加咨询，使用modelForm提交数据到数据库
    """

    def post(self, request):
        user_ask_form = UserAskForm(request.POST)
        if user_ask_form.is_valid():
            # modelForm可以直接提交到数据库,commit必须为true，才会保存到数据库，否则只是提交到数据库
            user_ask = user_ask_form.save(commit=True)
            # 异步请求AJAX,asynchonous js and xml
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json')


class OrgHomeView(View):
    def get(self, request, org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        # course_set,由外键反向找到course
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })


class OrgCourseView(View):
    def get(self, request, org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        # course_set,由外键反向找到course
        all_courses = course_org.course_set.all()[:3]
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })


class OrgDescView(View):
    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        # course_set,由外键反向找到course
        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })


class OrgTeacherView(View):
    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_teachers = course_org.teacher_set.all()
        # course_set,由外键反向找到course
        return render(request, 'org-detail-teachers.html', {
            'course_org': course_org,
            'current_page': current_page,
            'all_teachers': all_teachers,
            'has_fav': has_fav
        })


class AddFavView(View):
    """用户收藏"""
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        # 判断用户是否登录
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        else:
            # 拿出记录
            exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
            if exist_records:
                # 记录已经存在，表示用户取消收藏
                exist_records.delete()
                # 收藏数需要减1
                if fav_type == 1:
                    course = Course.objects.get(id=fav_id)
                    course.fav_nums -= 1
                    if course.fav_nums <= 0:
                        course.fav_nums = 0
                    course.save()
                elif fav_type == 2:
                    org = CourseOrg.objects.get(id=fav_id)
                    org.fav_nums -= 1
                    if org.fav_nums <= 0:
                        org.fav_nums = 0
                    org.save()
                elif fav_type == 3:
                    teacher = Teacher.objects.get(id=fav_id)
                    teacher.fav_nums -= 1
                    if teacher.fav_nums <= 0:
                        teacher.fav_nums = 0
                    teacher.save()
                return HttpResponse('{"status":"success","msg":"收藏"}', content_type='application/json')
            else:
                user_fav = UserFavorite()
                if int(fav_id) > 0 and int(fav_type) > 0:
                    user_fav.user = request.user
                    user_fav.fav_id = int(fav_id)
                    user_fav.fav_type = int(fav_type)
                    user_fav.save()

                # 收藏数加1
                if fav_type == 1:
                    course = Course.objects.get(id=fav_id)
                    course.fav_nums += 1
                    course.save()
                elif fav_type == 2:
                    org = CourseOrg.objects.get(id=fav_id)
                    org.fav_nums += 1
                    org.save()
                elif fav_type == 3:
                    teacher = Teacher.objects.get(id=fav_id)
                    teacher.fav_nums += 1
                    teacher.save()
                    return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
                else:
                    return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')


class TeacherList(View):
    def get(self, request):
        all_teachers = Teacher.objects.all()

        # 课程搜索, name__icontains：这个关键字可以拆分为四个部分，name表示的course表的name字段，
        # 双下滑线表示对这个字段做某种操作，i表示不区分大小写，contains表示做like查询
        # 整句的意思就是对传回来的关键字，生成select语句，用like来查询。
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_teachers = all_teachers.filter(Q(name__icontains=search_keywords) |\
                                               Q(work_company__icontains=search_keywords) |\
                                               Q(work_position__icontains=search_keywords) |\
                                               Q(points__icontains=search_keywords))

        # 标签筛选
        sort = request.GET.get('sort', '')
        if sort == 'hot':
            all_teachers = Teacher.objects.all().order_by('-click_nums')

        # 获取教师排行榜
        enumerate_recommend_teachers = self.get_recommend_teacher()


        # 使用工具类分页
        page_content = PaginatorUtils.paginator(request, all_teachers, 2, 'page')

        return render(request, 'teachers-list.html', {
            'all_teachers': all_teachers,
            'page_content': page_content,
            'enumerate_recommend_teachers': enumerate_recommend_teachers,
            'sort': sort
        })

    @staticmethod
    def get_recommend_teacher():
        # 推荐教师排行榜
        recommend_teachers = Teacher.objects.all().order_by('-fav_nums')[:3]
        enumerate_recommend_teachers = list(enumerate(recommend_teachers, start=1))
        return enumerate_recommend_teachers


class TeacherDetail(View):
    """
    教师详情信息
    """
    def get(self, request, teacher_id):

        this_teacher = Teacher.objects.get(id=int(teacher_id))

        # 教师点击量加1
        this_teacher.click_nums += 1
        this_teacher.save()

        # 通过外键反向查找课程
        # this_teacher_courses = this_teacher.course_set.all()

        # 通过Course Model筛选出该教师的课程，正向查找
        this_teacher_courses = Course.objects.filter(teacher=this_teacher)

        this_teacher_org = this_teacher.org

        # 推荐教师排行榜
        enumerate_recommend_teachers = TeacherList.get_recommend_teacher()

        # 收藏功能
        has_fav_teacher = False
        has_fav_org = False

        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=this_teacher.id, fav_type=3):
                has_fav_teacher = True
            if UserFavorite.objects.filter(user=request.user, fav_id=this_teacher_org.id, fav_type=2):
                has_fav_org = True

        return render(request, 'teacher-detail.html', {
            'this_teacher': this_teacher,
            'this_teacher_courses': this_teacher_courses,
            'this_teacher_org': this_teacher_org,
            'enumerate_recommend_teachers': enumerate_recommend_teachers,
            'has_fav_teacher': has_fav_teacher,
            'has_fav_org': has_fav_org
        })
