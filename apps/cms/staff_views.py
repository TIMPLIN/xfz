from django.shortcuts import render, reverse, redirect
from apps.xfzauth.models import User
from django.views.generic import View
from django.contrib.auth.models import Group
from apps.xfzauth.decorators import xfz_superuser_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from utils import restful
from django.core.paginator import Paginator


@method_decorator(xfz_superuser_required, name='dispatch')
class staffs_view(View):
    def get(self, request):
        page = int(request.GET.get('p', 1))

        staffs = User.objects.filter(is_staff=True)
        paginator = Paginator(staffs, 2)
        page_obj = paginator.page(page)

        context_data = self.get_paginator_data(paginator, page_obj)

        context = {
            'staffs': page_obj.object_list,
            'page_obj': page_obj,
            'paginator': paginator,
        }
        context.update(context_data)
        return render(request, 'cms/staffs.html', context=context)

    def get_paginator_data(self, paginator, page_obj, around_count = 2):
        current_page = page_obj.number
        num_pages = paginator.num_pages

        left_has_more = False
        right_has_more = False

        if current_page <= around_count + 2:
            left_pages = range(1, current_page)
        else:
            left_has_more = True
            left_pages = range(current_page - around_count, current_page)

        if current_page >= num_pages - around_count - 1:
            right_pages = range(current_page + 1, num_pages + 1)
        else:
            right_has_more = True
            right_pages = range(current_page + 1, current_page + around_count + 1)

        return {
            'left_pages' : left_pages,
            'right_pages' : right_pages,
            'left_has_more' : left_has_more,
            'right_has_more' : right_has_more,
            'current_page' : current_page,
            'num_pages' : num_pages
        }



@method_decorator(xfz_superuser_required, name='dispatch')
class AddStaffView(View):
    def get(self, request):
        groups = Group.objects.all()
        return render(request, 'cms/add_staff.html', locals())

    def post(self, request):
        telephone = request.POST.get('telephone')
        user = User.objects.filter(telephone=telephone).first()
        if user:
            user.is_staff = True
            group_ids = request.POST.getlist('groups')
            groups = Group.objects.filter(pk__in=group_ids)
            user.groups.set(groups)
            user.save()
            messages.info(request, '添加成功')
            return redirect(reverse('cms:staffs'))
        else:
            messages.warning(request, '该手机号码不存在')
            return redirect(reverse('cms:add_staff'))


@method_decorator(xfz_superuser_required, name='dispatch')
class EditStaffView(View):
    def get(self, request):
        staff_id = request.GET.get('staff_id')
        try:
            staff = User.objects.filter(pk=staff_id).first()
        except:
            messages.warning(request, '该职员不存在')
            return redirect(reverse('cms:staffs'))
        staff_groups = staff.groups.all()
        groups = Group.objects.all()
        return render(request, 'cms/add_staff.html', locals())

    def post(self, request):
        telephone = request.POST.get('telephone')
        user = User.objects.filter(telephone=telephone).first()
        if user:
            group_ids = request.POST.getlist('groups')
            if group_ids:
                groups = Group.objects.filter(pk__in=group_ids)
                user.groups.set(groups)
                user.save()
            else:
                user.is_staff = False
                user.groups.clear()
                user.save()
            messages.info(request, '修改成功')
            return redirect(reverse('cms:staffs'))
        else:
            messages.warning(request, '该手机号码不存在')
            return redirect(reverse('cms:staffs'))


def delete_staff(request):
    try:
        staff_pk = request.POST.get('staff_pk')
        User.objects.filter(uid=staff_pk).delete()
        return restful.ok()
    except:
        return restful.params_error(message='该员工不存在!')