from django.shortcuts import render, reverse
from .models import Course, CourseOrder
from django.http import Http404
from django.conf import settings
import time, os, hmac, hashlib
from utils import restful
from apps.xfzauth.decorators import xfz_login_required
from hashlib import md5
from django.views.decorators.csrf import csrf_exempt


def course_index(request):
    courses = Course.objects.all()
    return render(request, 'course/course_index.html', locals())


@xfz_login_required
def my_course(request):
    courses = Course.objects.filter(courseorder__buyer=request.user, courseorder__status=2).all()
    return render(request, 'course/my_course.html', locals())


@xfz_login_required
def course_detail(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
        buyed = CourseOrder.objects.filter(course=course, buyer=request.user, status=2).exists()
        return render(request, 'course/course_detail.html', locals())
    except Course.DoesNotExist:
        raise Http404


@xfz_login_required
def course_token(request):
    # video: 是视频文件的完整链接
    file = request.GET.get('video')
    course_id = request.GET.get('course_id')
    if not CourseOrder.objects.filter(course_id=course_id, buyer=request.user, status=2).exists():
        return restful.params_error(message='请先购买课程!')

    expiration_time = int(time.time()) + 2 * 60 * 60

    USER_ID = settings.BAIDU_CLOUD_USER_ID
    USER_KEY = settings.BAIDU_CLOUD_USER_KEY

    extension = os.path.splitext(file)[1]
    media_id = file.split('/')[-1].replace(extension, '')

    key = USER_KEY.encode('utf-8')
    message = '/{}/{}'.format(media_id, expiration_time).encode('utf-8')
    signature = hmac.new(key, message, digestmod=hashlib.sha256).hexdigest()
    token = '{}_{}_{}'.format(signature, USER_ID, expiration_time)
    return restful.result(data={'token': token})


@xfz_login_required
def course_order(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)

        goods = {
            'thumbnail': course.cover_url,
            'title': course.title,
            'price': course.price
        }
        order = CourseOrder.objects.create(course=course, buyer=request.user, amount=course.price, status=1)

        notify_url = request.build_absolute_uri(reverse('course:notify_view'))
        return_url = request.build_absolute_uri(reverse('course:course_detail', args=(course.id,)))

        return render(request, 'course/goods_order.html', locals())
    except Course.DoesNotExist:
        raise Http404


@xfz_login_required
def course_order_key(request):
    goodsname = request.POST.get('goodsname')
    istype = request.POST.get('istype')
    notify_url = request.POST.get('notify_url')
    orderid = request.POST.get('orderid')
    price = request.POST.get('price')
    return_url = request.POST.get('return_url')

    token = 'd033ee503d74498c328602cedccdbeac'
    uid = '9da89bbf6a37ac6789b4acab'

    orderuid = str(request.user.pk)
    key = md5((goodsname + istype + notify_url + orderid + orderuid + price + return_url + token + uid).encode('utf-8')).hexdigest()
    return restful.result(data={'key': key})


@csrf_exempt
def notify_view(request):
    orderid = request.POST.get('orderid')
    CourseOrder.objects.filter(pk=orderid).update(status=2)
    return restful.ok()
