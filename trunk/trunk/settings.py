"""
Django settings for trunk project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import configparser

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v+_we$4exdk-qzczegu(57$2*i6b@k_5@0!7%a^u#*nc$%=qyd'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_oss_storage',
    'rest_framework',
    'rest_framework_jwt',
    'django_filters',
    'easyaudit',
    'drf_yasg',
    'ncore.apps.NcoreConfig',
    'approvalflow',
    'dingtalkapi',
    'entwechatapi',
    'wechatminiprogramapi',
    # 'silk',
    # 'elasticapm.contrib.django',
]

ELASTIC_APM = {
    'SERVICE_NAME': 'gasproject',
    #'SECRET_TOKEN': '',
    'SERVER_URL': 'http://192.168.1.233:8200',
    'DJANGO_TRANSACTION_NAME_FROM_ROUTE': True,
    'DEBUG': True,
}


MIDDLEWARE = [
    #'elasticapm.contrib.django.middleware.TracingMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'silk.middleware.SilkyMiddleware',
    'easyaudit.middleware.easyaudit.EasyAuditMiddleware',
]

ROOT_URLCONF = 'trunk.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.i18n',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'trunk.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

CNF_DIR = './trunk/demo.cnf'
conf = configparser.ConfigParser()
conf.read(CNF_DIR)

APPID = conf.get('miniprogram', 'appid')
SECRET = conf.get('miniprogram', 'secret')

"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': CNF_DIR,
        },
    }
}
"""

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

REST_FRAMEWORK = {

    'DATETIME_FORMAT': "%Y-%m-%d %H:%M:%S",
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
    ),
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_PAGINATION_CLASS': 'ncore.paginations.CustomerPagination',
    'PAGE_SIZE': 30,
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'ncore.authentications.CsrfExemptSessionAuthentication',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.JSONParser',
    ),
    'EXCEPTION_HANDLER': 'ncore.exceptions.custom_exception_handler',

}

SESSION_COOKIE_HTTPONLY = True  # this is default value

SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # this is the default value

SESSION_SAVE_EVERY_REQUEST = True  # update last activity time to now

SESSION_COOKIE_AGE = 3600 * 2  # 120 mins


DJANGO_EASY_AUDIT_WATCH_REQUEST_EVENTS = False

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

from .settings_swagger import *

# 测试环境及部分项目不需要使用oss
if (not DEBUG) and 0:
    OSS_ACCESS_KEY_ID = conf.get('oss', 'appid')
    OSS_ACCESS_KEY_SECRET = conf.get('oss', 'secret')
    from .settings_oss import *

# from .settings_jwt import *
# AUTH_USER_MODEL = "ncore.User"

if "silk" in INSTALLED_APPS:
    DJANGO_EASY_AUDIT_UNREGISTERED_CLASSES_EXTRA = ["silk.Request", "silk.Response",
    "silk.SQLQuery", "silk.Profile"]

SILKY_AUTHENTICATION = True  # User must login
LOGIN_URL = 'rest_framework:login'

"""
TRACER_SERVICE_NAME = 'demo'


TRACER_CONFIG = {
    'sampler': {
        'type': 'const',
        'param': 1,
    },
    'local_agent': {
        'reporting_host': 'localhost',
    },
    'trace_id_header': 'trace-id',
    'baggage_header_prefix': 'jaegertrace-',
}
"""

