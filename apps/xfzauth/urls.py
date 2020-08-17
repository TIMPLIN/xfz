from django.urls import path
from . import views

app_name = 'xfzauth'

urlpatterns = [
    path('register/', views.register, name = 'register'),
    path('login/', views.login_view, name = 'login'),
    path('logout/', views.logout_view, name='logout'),
    path('img_captcha/', views.img_captcha, name='img_captcha'),
    path('sms_captcha/', views.sms_captcha, name='sms_captcha'),
    path('userinfo/', views.AddUserInfoView.as_view(), name='add_userinfo'),
    path('edit_userinfo/', views.EditUserInfoView.as_view(), name='edit_userinfo'),
]