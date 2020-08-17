"""
Django settings for xfz project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=9-1)l^9j(*1114jwqv)g8&v-ubu_ce$zrtn404%njh2dp+uy2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1','192.168.0.112']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'apps.news',
    'apps.cms',
    'apps.xfzauth',
    'apps.ueditor',
    'rest_framework',
    'debug_toolbar',
    'apps.course',
    'apps.payinfo',
    'haystack',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'xfz.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'front', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'builtins': [
                'django.templatetags.static'
            ]
        },
    },
]

WSGI_APPLICATION = 'xfz.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'xfz',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': 'root',
    }
}



# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


AUTH_USER_MODEL = 'xfzauth.User'


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

CACHES = {
    'default': {
		'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
		'LOCATION': '127.0.0.1:11211',
	}
}


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_dist')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'front', 'dist')
]


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


UEDITOR_UPLOAD_TO_SERVER = True
UEDITOR_UPLOAD_PATH = MEDIA_ROOT
UEDITOR_CONFIG_PATH = os.path.join(BASE_DIR, 'front', 'dist', 'ueditor', 'config.json')



QINIU_ACCESS_KEY = '-A38BYoSGl-hGGagX70EpFtnHQqBj0nd_AAkp7YO'
QINIU_SECRET_KEY = 'IreMY5lp1kXdHKAuu83UvLoQPtqh-Nrs8DtB1ftq'
QINIU_BUCKET_NAME = ''
QINIU_DOMAIN = ''


#UEDITOR_UPLOAD_TO_QINIU = True
#UEDITOR_QINIU_ACCESS_KEY = QINIU_ACCESS_KEY
#UEDITOR_QINIU_SECRET_KEY = QINIU_SECRET_KEY
#UEDITOR_QINIU_BUCKET_NAME = QINIU_BUCKET_NAME
#UEDITOR_QINIU_DOMAIN = QINIU_DOMAIN



#一次加载多少篇文章
ONE_PAGE_NEWS_COUNT = 2



INTERNAL_IPS = ['127.0.0.1']
DEBUG_TOOLBAR_PANELS = [
    #哪个版本的django
    'debug_toolbar.panels.versions.VersionsPanel',

    #计时，判断加载当前页面所花的时间
    'debug_toolbar.panels.timer.TimerPanel',

    #读取django的配置信息
    'debug_toolbar.panels.settings.SettingsPanel',

    #当前请求头和响应头信息
    'debug_toolbar.panels.headers.HeadersPanel',

    #当前请求的响应信息(视图函数，Cookie信息，Session信息等)
    'debug_toolbar.panels.request.RequestPanel',

    #查看SQL语句
    'debug_toolbar.panels.sql.SQLPanel',

    #静态文件
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',

    #模板文件
    'debug_toolbar.panels.templates.TemplatesPanel',

    #缓存
    'debug_toolbar.panels.cache.CachePanel',

    #信号
    'debug_toolbar.panels.signals.SignalsPanel',

    #日志
    'debug_toolbar.panels.logging.LoggingPanel',

    #重定向
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': '',
}



BAIDU_CLOUD_USER_ID = '7e2957ab34f54fd2aa5becf013a5e287'
BAIDU_CLOUD_USER_KEY = '1a589ce2f4df4392' 



HAYSTACK_CONNECTIONS = {
    'default':{
        #'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',

        # 设置haystack的搜索引擎
        'ENGINE': 'apps.news.whoosh_cn_backend.WhooshEngine',
        # 设置索引文件的位置
        'PATH': os.path.join(BASE_DIR, 'whoosh_index')
    }
}
#增删改查操作后自动更新索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'


CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_SERIALIZER = 'json'