from django.urls import path
from . import views, course_views, staff_views

app_name = 'cms'

urlpatterns = [
    path('index/', views.index, name = 'index'),

    path('news_category/', views.news_category, name = 'news_category'),
    path('add_news_category/', views.add_news_category, name = 'add_news_category'),
    path('edit_news_category/', views.edit_news_category, name = 'edit_news_category'),
    path('delete_news_category/', views.delete_news_category, name = 'delete_news_category'),

    path('upload_file/', views.upload_file, name = 'upload_file'),
    path('qntoken/', views.qntoken, name = 'qntoken'),

    path('banners/', views.banners, name = 'banners'),
    path('add_banner/', views.add_banner, name = 'add_banner'),
    path('banner_list/', views.banner_list, name = 'banner_list'),
    path('delete_banner/', views.delete_banner, name = 'delete_banner'),
    path('edit_banner/', views.edit_banner, name = 'edit_banner'),

    path('write_news/', views.WriteNewsView.as_view(), name = 'write_news'),
    path('news_list/', views.NewsListView.as_view(), name = 'news_list'),
    path('edit_news/', views.EditNewsView.as_view(), name = 'edit_news'),
    path('delete_news/', views.delete_news, name = 'delete_news'),
]


urlpatterns += [
    path('pub_course/', course_views.PubCourseView.as_view(), name='pub_course'),
    path('course_list/', course_views.CourseListView.as_view(), name='course_list'),
    path('edit_course/', course_views.EditCourseView.as_view(), name='edit_course'),
    path('delete_course/', course_views.delete_course, name='delete_course'),

    path('course_category/', course_views.course_category, name='course_category'),
    path('add_course_category/', course_views.add_course_category, name='add_course_category'),
    path('edit_course_category/', course_views.edit_course_category, name='edit_course_category'),
    path('delete_course_category/', course_views.delete_course_category, name='delete_course_category'),
]


urlpatterns += [
    path('staffs/', staff_views.staffs_view.as_view(), name='staffs'),
    path('add_staff/', staff_views.AddStaffView.as_view(), name='add_staff'),
    path('edit_staff/', staff_views.EditStaffView.as_view(), name='edit_staff'),
    path('delete_staff/', staff_views.delete_staff, name='delete_staff'),
]