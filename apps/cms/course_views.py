from django.shortcuts import render
from .forms import PubCourseForm, EditCourseCategoryForm
from apps.course.models import Course, Teacher, CourseCategory
from django.views.generic import View
from utils import restful
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from apps.cms.forms import EditCourseForm
from urllib import parse
from datetime import datetime
from django.core.paginator import Paginator
from django.utils.timezone import make_aware


@method_decorator(permission_required(perm=['course.change_course', 'course.add_course'], login_url='/'), name='dispatch')
class PubCourseView(View):
    def get(self, request):
        categories = CourseCategory.objects.all()
        teachers = Teacher.objects.all()
        return render(request, 'cms/pub_course.html', locals())

    def post(self, request):
        form = PubCourseForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            category_id = form.cleaned_data.get('category_id')
            video_url = form.cleaned_data.get('video_url')
            cover_url = form.cleaned_data.get('cover_url')
            price = form.cleaned_data.get('price')
            duration = form.cleaned_data.get('duration')
            profile = form.cleaned_data.get('profile')
            teacher_id = form.cleaned_data.get('teacher_id')

            category = CourseCategory.objects.get(pk=category_id)
            teacher = Teacher.objects.get(pk=teacher_id)

            Course.objects.create(title=title, category=category, video_url=video_url, cover_url=cover_url, price=price, duration=duration, profile=profile, teacher=teacher)

            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())


@require_POST
@permission_required(perm='course.delete_course', login_url='/')
def delete_course(request):
    course_id = request.POST.get('course_id')
    Course.objects.filter(pk=course_id).delete()
    return restful.ok()


@method_decorator(permission_required(perm=['course.add_course', 'course.delete_course'], login_url='/'), name='dispatch')
class EditCourseView(View):
    def get(self, request):
        course_id = request.GET.get('course_id')
        course = Course.objects.get(pk=course_id)
        context = {
            'course': course,
            'categories': CourseCategory.objects.all(),
            'teachers': Teacher.objects.all()
        }
        return render(request, 'cms/pub_course.html', context=context)

    def post(self, request):
        form = EditCourseForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            category_id = form.cleaned_data.get('category')
            video_url = form.cleaned_data.get('video_url')
            cover_url = form.cleaned_data.get('cover_url')
            price = form.cleaned_data.get('price')
            duration = form.cleaned_data.get('duration')
            profile = form.cleaned_data.get('profile')
            teacher_id = form.cleaned_data.get('teacher_id')
            pk = form.cleaned_data.get('pk')

            category = CourseCategory.objects.get(pk=category_id)
            teacher = Teacher.objects.get(pk=teacher_id)
            Course.objects.filter(pk=pk).update(title=title, video_url=video_url, cover_url=cover_url, price=price, duration=duration, profile=profile, category=category, teacher=teacher)

            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())


@method_decorator(permission_required(perm=['course.add_course', 'course.change_course'], login_url='/'), name='dispatch')
class CourseListView(View):
    def get(self, request):
        page = int(request.GET.get('p', 1))
        start = request.GET.get('start')
        end = request.GET.get('end')
        title = request.GET.get('title')

        category_id = int(request.GET.get('category', 0) or 0)

        categories = CourseCategory.objects.all()
        courses = Course.objects.select_related('author', 'category')

        if start or end:
            if start:
                start_date = datetime.strptime(start, '%Y/%m/%d')
            else:
                start_date = datetime(year=2017, month=4, day=21)

            if end:
                end_date = datetime.strptime(end, '%Y/%m/%d')
            else:
                end_date = datetime.today()
            courses = courses.filter(pub_time__range=(make_aware(start_date), make_aware(end_date)))

        if title:
            courses = courses.filter(title__icontains=title)
        if category_id:
            courses = courses.filter(category=category_id)

        paginator = Paginator(courses, 2)
        page_obj = paginator.page(page)

        context_data = self.get_paginator_data(paginator, page_obj)

        context = {
            'categories': categories,
            'newses': page_obj.object_list,
            'page_obj': page_obj,
            'paginator': paginator,
            'start':start,
            'end': end,
            'title': title,
            'category_id': category_id,
            'url_query': '&'+ parse.urlencode({
                'start': start or '',
                'end': end or '',
                'title': title or '',
                'category': category_id or '',
            })
        }
        context.update(context_data)
        return render(request, 'cms/course_list.html', context=context)

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




def course_category(request):
    categories = CourseCategory.objects.all()
    return render(request, 'cms/course_category.html', locals())


def add_course_category(request):
    name = request.POST.get('name')
    if not CourseCategory.objects.filter(name=name).exists():
        CourseCategory.objects.create(name=name)
        return restful.ok()
    else:
        return restful.params_error(message='该分类已存在')


def edit_course_category(request):
    form = EditCourseCategoryForm(request.POST)
    if form.is_valid():
        course_id = form.cleaned_data.get('pk')
        name = form.cleaned_data.get('name')
        try:
            CourseCategory.objects.filter(id=course_id).update(name=name)
            return restful.ok()
        except:
            restful.params_error(message='该分类不存在')
    else:
        return restful.params_error(message=form.get_errors())


def delete_course_category(request):
    course_id = request.POST.get('course_id')
    try:
        CourseCategory.objects.filter(pk=course_id).delete()
        return restful.ok()
    except:
        return restful.params_error(message='该分类不存在')