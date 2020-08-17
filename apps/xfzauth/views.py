from django.contrib.auth import logout, login, authenticate
from django.views.decorators.http import require_POST
from .forms import LoginForm, RegisterForm, UserInfoForm
from .models import UserInfo
from utils import restful
from django.shortcuts import redirect, reverse
from utils.captcha.xfzcaptcha import Captcha
from io import BytesIO
from django.http import HttpResponse
from django.core.cache import cache
from django.contrib.auth import get_user_model
from utils.aliyunsdk import aliyunsms
from django.views.generic import View
from django.shortcuts import render
from .decorators import xfz_login_required
from django.utils.decorators import method_decorator


User = get_user_model()


@require_POST
def login_view(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        password = form.cleaned_data.get('password')
        remember = form.cleaned_data.get('remember')
        user = authenticate(request, username=telephone, password=password)
        if user:
            if user.is_active:
                login(request, user)
                if remember:
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)
                return restful.ok()
            else:
                return restful.unauth_error(message='你的账号已被冻结!')
        else:
            return restful.params_error(message='手机号或密码错误!')
    else:
        return restful.params_error(message=form.get_errors())


def logout_view(request):
    logout(request)
    return redirect(reverse('index'))


@require_POST
def register(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = User.objects.create_user(telephone=telephone, username=username, password=password)
        login(request, user)
        return restful.ok()
    else:
        return restful.params_error(message=form.get_errors())


def img_captcha(request):
    text, image = Captcha.gene_code()
    #BytesIO相当于一个管道,用来存储图片二进制流数据,生成一个流对象
    out = BytesIO()

    #将image对象保存到BytesIO中
    image.save(out, 'png')

    #将BytesIO的文件指针移动到最开始的位置
    out.seek(0)

    #从BytesIO的管道中，读取图片数据，保存到response对象上
    response = HttpResponse(content_type='image/png')

    response.write(out.read())
    response['Content-length'] = out.tell()

    cache.set(text.lower(), text.lower(), 5*60)
    print("图片验证码: %s" % text)

    return response


def sms_captcha(request):
    telephone = request.GET.get('telephone')
    code = Captcha.gene_text()
    cache.set(telephone, code, 5*60)
    #aliyunsms.send_sms(telephone, code=code)
    print("短信验证码: %s" % code)
    return restful.ok()




@method_decorator(xfz_login_required, name='dispatch')
class AddUserInfoView(View):
    def get(self, request):
        return render(request, 'user/userinfo.html', locals())

    def post(self, request):
        form = UserInfoForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            address = form.cleaned_data.get('address')
            school = form.cleaned_data.get('school')
            company = form.cleaned_data.get('company')
            signature = form.cleaned_data.get('signature')
            user = request.user
            user.email = email
            user.save()
            UserInfo.objects.create(school=school, company=company, address=address, signature=signature, user=request.user)
            return restful.ok()
        else:
            restful.params_error(form.get_errors())




@method_decorator(xfz_login_required, name='dispatch')
class EditUserInfoView(View):
    def get(self, request):
        userinfo_id = request.GET.get('userinfo_id')
        userinfo = UserInfo.objects.get(pk = userinfo_id)
        return render(request, 'user/userinfo.html', locals())

    def post(self, request):
        form = UserInfoForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            address = form.cleaned_data.get('address')
            school = form.cleaned_data.get('school')
            company = form.cleaned_data.get('company')
            signature = form.cleaned_data.get('signature')
            user = request.user
            user.email = email
            user.save()
            UserInfo.objects.create(school=school, company=company, address=address, signature=signature, user=request.user)
            return restful.ok()
        else:
            restful.params_error(form.get_errors())