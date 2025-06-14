"""
Django settings for async_mysql_project project.

Generated by 'django-admin startproject' using Django 5.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-=xaq%c^1lnt$yl#77e*!epnwv5s_w*3^c_j*4c@xs4srqodz66'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Добавляем AccountMiddleware от allauth
    'allauth.account.middleware.AccountMiddleware',
    # 'whitenoise.middleware.WhiteNoiseMiddleware',  # Эта строка решает проблема поиска статических файлов
]

ROOT_URLCONF = 'async_mysql_project.urls'

import os

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Указываем на папку с шаблонами
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'async_mysql_project.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

import json
project_dir = os.path.dirname(os.path.abspath(__file__))
folder_path = os.path.join(project_dir, '..', '..')
folder_path = os.path.abspath(folder_path)
# Открываем файл и загружаем данные
with open(f'{folder_path}//general_settings.json', 'r', encoding='utf-8-sig') as file:
    json_object = json.load(file)

# Настройки Celery
CELERY_BROKER_URL = f'redis://{json_object['host']}:6379/0'  # Указываем Redis как брокер
CELERY_RESULT_BACKEND = f'redis://{json_object['host']}:6379/0'  # Указываем Redis для хранения результатов задач

# Опционально: таймауты для выполнения задач
CELERY_TIMEZONE = 'UTC'
CELERY_ACCEPT_CONTENT = ['json']  # Используем JSON для кодирования
CELERY_TASK_SERIALIZER = 'json'

# Прочие настройки
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60  # Тайм-аут на выполнение задачи (30 минут)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "data_app/static",
]

# Папка для сбора статических файлов в продакшн (если необходимо)
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Если хотите хранить файлы в папке 'file' внутри проекта:
MEDIA_ROOT = os.path.join(BASE_DIR, "")

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'INFO',
#             'class': 'logging.FileHandler',
#             'filename': 'user_actions.log',
#             'encoding': 'utf-8',  # Устанавливаем кодировку UTF-8
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'INFO',
#             'propagate': True,
#         },
#     },
# }

"""------------------------------------------------------"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': f'{json_object['base_name']}',
        'USER': f'{json_object['user']}',
        'PASSWORD': f'{json_object['password']}',
        'HOST': f'{json_object['host']}',  # или IP, если база на удалённом сервере
        'PORT': '3306',
        # 'OPTIONS': {
        #     'charset': 'utf8mb4',
        # },
    }
}

"""ОТКЛЮЧИТЬ ОТПРАВКУ НА ПОЧТУ И ПОДТВЕРЖДЕНИЕ"""
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
ACCOUNT_EMAIL_VERIFICATION = 'none'

# Добавляем конфигурации для Channels
ASGI_APPLICATION = 'async_mysql_project.asgi.application'

# Канальные слои, если вам нужны, например, WebSockets
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}

# Application definition
# Подключаем Allauth
INSTALLED_APPS = [
    # другие приложения
    'django.contrib.sites',  # требуется для Allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',  # для примера, можно добавить другие
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # другие приложения
    'data_app',  # ваше приложение с моделью
    'channels',
]

LOGOUT_REDIRECT_URL = '/accounts/login/'  # Укажите правильный путь к вашей странице входа

SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

LOGIN_REDIRECT_URL = '/'
