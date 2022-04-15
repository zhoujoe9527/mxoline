import json
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import View
# Create your views here.
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm, UserInfoForm
from django.contrib.auth.hashers import make_password

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect

from apps.utils.email_send import send_email
from apps.utils.mixin_utils import LoginRequiredMixin
from .forms import ChangeUserAvatarForm
from .models import UserProfile, EmailVerifyRecord, Banner
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from courses.models import Course
from utils.PaginatorUtils import PaginatorUtils


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


# 基于类实现登录。类会自动检查是post还是get类型
class LoginView(View):
    def get(self, request):
        # request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            # 返回一个对象，不为空，用户和密码是正确的
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    from django.urls import reverse
                    return HttpResponseRedirect(reverse('index'))
                    # return render(request, request.session['login_from'])
                else:
                    return render(request, "login.html", {"msg": "用户未激活"})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误"})
        else:
            return render(request, "login.html", {"login_form": login_form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        from django.urls import reverse
        return HttpResponseRedirect(reverse('index'))


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 基于方法实现登录
# def user_login(request):
#     if request.method == "POST":
#         user_name = request.POST.get("username", "")
#         pass_word = request.POST.get("password", "")
#         #返回一个对象，不为空，用户和密码是正确的
#         user = authenticate(username=user_name, password=pass_word)
#         if user is not None:
#             login(request, user)
#             return render(request, "index.html")
#         else:
#             return render(request, "login.html", {})
#     elif request.method == "GET":
#         return render(request, "login.html", {})


class RegisterView(View):

    def get(self, request):
        register_form = RegisterForm()  # 这里传值是为了显示验证码
        # 第三个参数用法
        return render(request, "register.html", {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email_1', "")
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {'register_form': register_form, 'msg': '用户已存在'})
            user_password = request.POST.get('password', "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            # 密码需要加密
            user_profile.password = make_password(user_password)
            user_profile.save()

            send_email(user_name, "register")
        else:
            return render(request, "register.html", {'register_form': register_form})


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetPwdForm()
        return render(request, "forgetpwd.html", {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', "")
            if not UserProfile.objects.filter(email=email):
                return render(request, "forgetpwd.html", {'msg': u"用户不存在"})
            send_email(email, 'forget')
            return render(request, "send_success.html")
        else:
            return render(request, "forgetpwd.html", {'forget_form': forget_form})


class ResetView(View):
    def get(self, request, reset_code):
        all_records = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {"email": email})
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', "")
            pwd2 = request.POST.get('password2', "")
            email = request.POST.get('email', "")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email": email, "msg": u"密码不一致"})

            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()

            return render(request, "login.html")
        else:
            email = request.POST.get('email', "")
            return render(request, "password_reset.html", {"email": email, "modify_form": modify_form})


class UsersInfo(LoginRequiredMixin, View):
    """
    个人信息显示
    """
    def get(self, request):
        return render(request, 'usercenter-info.html', {})

    def post(self, request):
        # 如果不指定实例对象，直接保存，会新创建一个用户
        # 这里使用modelForm修改数据，因为用户修改的数据不需要做逻辑判断，不像修改邮箱，需要
        # 判断验证码，修改类型等信息，用户个人信息修改后，在js中做简单判断，就可以直接存入数据库
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UserChangeAvatar(View):
    """
    用户更换头像
    """
    def post(self, request):
        user_image_form = ChangeUserAvatarForm(request.POST, request.FILES, instance=request.user)
        if user_image_form.is_valid():
            user_image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"修改头像失败"}', content_type='application/json')


class UpdatePwd(LoginRequiredMixin, View):
    """
    在已登录状态下，在个人中心修改密码
    """
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', "")
            pwd2 = request.POST.get('password2', "")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail", "msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd1)
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendUpdateEmailCode(LoginRequiredMixin, View):
    """
    发送修改邮箱验证码
    """
    def get(self, request):
        new_email = request.GET.get('email', '')

        # 验证邮箱为空在js里面已经做好
        if UserProfile.objects.filter(email=new_email):
            return HttpResponse('{"email":"邮箱已经存在"}', content_type='application/json')
        else:
            send_status = send_email(new_email, "update_email")
            if send_status:
                return HttpResponse('{"status":"success"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"发送验证码失败，请重试"}', content_type='application/json')


class UpdateEmail(View):
    """
    修改用户邮箱
    """
    def post(self, request):
        update_email_code = request.POST.get('code', '')
        new_email = request.POST.get('email', '')

        exist_records = EmailVerifyRecord.objects.filter(email=new_email, code=update_email_code, send_type='update_email')
        if exist_records:
            # request.user 是UserProfile对象
            user = request.user
            user.email = new_email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"验证码出错"}', content_type='application/json')


class UserMyCourse(LoginRequiredMixin, View):
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)

        return render(request, 'usercenter-mycourse.html', {
            'user_courses': user_courses
        })


class UserFavoriteCourse(LoginRequiredMixin, View):
    def get(self, request):
        user_fav_records = UserFavorite.objects.filter(user=request.user, fav_type=1)
        fav_course_ids = [user_fav_record.fav_id for user_fav_record in user_fav_records]
        user_fav_courses = Course.objects.filter(id__in=fav_course_ids)
        return render(request, 'usercenter-fav-course.html', {
            'user_fav_courses': user_fav_courses
        })


class UserFavoriteOrg(LoginRequiredMixin, View):
    def get(self, request):
        user_fav_records = UserFavorite.objects.filter(user=request.user, fav_type=2)
        fav_org_ids = [user_fav_record.fav_id for user_fav_record in user_fav_records]
        user_fav_org = CourseOrg.objects.filter(id__in=fav_org_ids)
        return render(request, 'usercenter-fav-org.html', {
            'user_fav_org': user_fav_org
        })


class UserFavoriteTeacher(View):
    def get(self, request):
        user_fav_records = UserFavorite.objects.filter(user=request.user, fav_type=3)
        fav_teacher_ids = [user_fav_record.fav_id for user_fav_record in user_fav_records]
        user_fav_teachers = Teacher.objects.filter(id__in=fav_teacher_ids)
        return render(request, 'usercenter-fav-teacher.html', {
            'user_fav_teachers': user_fav_teachers
        })


class UserReadMessage(View):
    def get(self, request):
        user_message = UserMessage.objects.filter(user=request.user.id)

        # 当点击该界面时，应该将信息的状态设置为已读，并减少提示未读的信息数
        user_unread_message = UserMessage.objects.filter(user=request.user.id, is_read=False)
        for per_unread_message in user_unread_message:
            per_unread_message.is_read = True
            per_unread_message.save()

        # 分页
        per_user_message = PaginatorUtils.paginator(request, user_message, 5)
        return render(request, 'usercenter-message.html', {
            'per_user_message': per_user_message
        })


class Index(View):
    def get(self, request):
        # 首页轮播信息
        banner_info = Banner.objects.all().order_by('index')

        # 首页轮播公开课程
        banner_course = Course.objects.filter(is_banner=True)[:5]

        # 首页公开课课程
        course = Course.objects.filter(is_banner=False)[:6]

        # 首页课程机构
        all_org = CourseOrg.objects.all()

        return render(request, 'index.html', {
            'banner_info': banner_info,
            'banner_course': banner_course,
            'course': course,
            'all_org': all_org
        })
