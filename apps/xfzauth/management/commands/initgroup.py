#https://docs.djangoproject.com/zh-hans/2.0/howto/custom-management-commands/

from django.core.management.base import BaseCommand

from django.contrib.auth.models import Group, Permission, ContentType
from apps.news.models import News, Comment, NewsCategory, Banner
from apps.course.models import CourseCategory, Course, Teacher, CourseOrder
from apps.payinfo.models import Payinfo, PayinfoOrder


class Command(BaseCommand):
    def handle(self, *args, **options):
        #1.编辑组（管理新闻, 管理课程, 管理评论, 管理轮播图等）
        edit_content_types = [
            ContentType.objects.get_for_model(News),
            ContentType.objects.get_for_model(NewsCategory),
            ContentType.objects.get_for_model(Comment),
            ContentType.objects.get_for_model(Banner),
            ContentType.objects.get_for_model(Teacher),
            ContentType.objects.get_for_model(Course),
            ContentType.objects.get_for_model(CourseCategory),
            ContentType.objects.get_for_model(Payinfo),
        ]
        edit_permissions = Permission.objects.filter(content_type__in=edit_content_types)
        editGroup = Group.objects.create(name='编辑')
        editGroup.permissions.set(edit_permissions)
        editGroup.save()
        self.stdout.write(self.style.SUCCESS('编辑组创建完成'))

        #2.财务组（课程订单, 付费资讯订单等）
        finance_content_types = [
            ContentType.objects.get_for_model(CourseOrder),
            ContentType.objects.get_for_model(PayinfoOrder),
        ]
        finance_permissions = Permission.objects.filter(content_type__in=finance_content_types)
        finaceGroup = Group.objects.create(name='财务')
        finaceGroup.permissions.set(finance_permissions)
        finaceGroup.save()
        self.stdout.write(self.style.SUCCESS('财务组创建完成'))

        #3.管理员组（编辑组 + 财务组）
        admin_permissions = edit_permissions.union(finance_permissions)
        adminGroup = Group.objects.create(name='管理员')
        adminGroup.permissions.set(admin_permissions)
        adminGroup.save()
        self.stdout.write(self.style.SUCCESS('管理员组创建完成'))

        #4.超级管理员