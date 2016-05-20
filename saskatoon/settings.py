#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Django settings for saskatoon project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')ls=exy4%bo$^glzer6li-^&(zw&+c&(p!n@x)d4$aaaal^chm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'bootstrap3_datepicker',
    'suit',
    'dal',
    'dal_select2',
    'django_filters',
    # 'grappelli',
    # 'djangocms_admin_style',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'saskatoon',
    'user_profile',
    'django_extensions',
    'bootstrap3',
    'django_forms_bootstrap',
    'crispy_forms',
    # 'happenings',
    # 'django_bootstrap_calendar',
    'simple_history',
#    'easymode',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
)

ROOT_URLCONF = 'saskatoon.urls'

WSGI_APPLICATION = 'saskatoon.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/
from django.utils.translation import gettext_lazy as _

TIME_ZONE = 'America/Montreal'
#LANGUAGE_CODE = 'en'
LANGUAGE_CODE = 'fr'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = (
    ('fr', _('Français')),
    ('en', _('English')),
)

DEFAULT_LANGUAGE = 1 

LOCALE_PATHS = (
    os.path.join('locale/'),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
#STATIC_ROOT = 'saskatoon/static/'

STATICFILES_DIRS = (
    os.path.join(os.path.dirname(__file__),'static'),
)

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates').replace('\\', '/'),
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

AUTH_USER_MODEL = "user_profile.AuthUser"

CRISPY_TEMPLATE_PACK = 'bootstrap3'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    "django.core.context_processors.i18n", 
)

MIGRATION_MODULES = {'django_extensions': None}

SUIT_CONFIG = {
    'ADMIN_NAME': 'Saskatoon',
    'MENU_EXCLUDE': ('auth.group', 'auth'),
    }

# FIXME: options to make database translatable
#PROJECT_DIR = os.path.dirname('saskatoon')
#MASTER_SITE = True
#AUTO_CATALOG = False

