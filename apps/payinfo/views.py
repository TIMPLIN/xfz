from django.shortcuts import render, reverse
from .models import Payinfo, PayinfoOrder
from apps.xfzauth.decorators import xfz_login_required
from utils import restful
from django.conf import settings
from django.http import Http404, FileResponse
import os
from django.views.decorators.csrf import csrf_exempt



def index(request):
    payinfos = Payinfo.objects.all()
    return render(request, 'payinfo/payinfo.html', locals())


@xfz_login_required
def my_payinfo(request):
    payinfos = Payinfo.objects.filter(payinfoorder__buyer=request.user, payinfoorder__status=2).all()
    return render(request, 'payinfo/my_payinfo.html', locals())


@xfz_login_required
def payinfo_order(request):
    payinfo_id = request.GET.get('payinfo_id')
    payinfo = Payinfo.objects.get(pk=payinfo_id)
    order = PayinfoOrder.objects.create(payinfo=payinfo, buyer=request.user, amount=payinfo.price, status=1)

    goods = {
        'thumbnail':'',
        'title': payinfo.title,
        'price': payinfo.price
    }
    notify_url = request.build_absolute_uri(reverse('payinfo:notify_view'))
    return_url = request.build_absolute_uri(reverse('payinfo:payinfo_index'))

    return render(request, 'course/goods_order.html', locals())


@csrf_exempt
def notify_view(request):
    orderid = request.POST.get('orderid')
    PayinfoOrder.objects.filter(pk=orderid).update(status=2)
    return restful.ok()


@xfz_login_required
def download(request):
    payinfo_id = request.GET.get('payinfo_id')
    order = PayinfoOrder.objects.filter(payinfo_id=payinfo_id, buyer=request.user, status=2).first()
    if order:
        payinfo = order.payinfo
        path = os.path.join(settings.MEDIA_ROOT, payinfo.path)
        fp = open(path, 'rb')
        response = FileResponse(fp)
        response['Content-Type'] = 'image/jpeg'
        response['Content-Disposition'] = "attachment;filename='%s'" % path.split('/')[-1]
        return response
    else:
        raise Http404()