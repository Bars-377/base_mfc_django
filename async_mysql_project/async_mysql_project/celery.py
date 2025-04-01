from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Устанавливаем настройки по умолчанию для Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'async_mysql_project.settings')

app = Celery('async_mysql_project', broker="redis://localhost:6379/0")

# Используем настройки из Django (это важно для конфигурации Celery)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически открывать все задачи из всех установленных Django приложений
app.autodiscover_tasks()
