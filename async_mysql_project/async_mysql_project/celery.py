# async_mysql_project/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Устанавливаем Django settings модуль
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'async_mysql_project.settings')

app = Celery('async_mysql_project')

# Используем настройки Celery из файла settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически обнаруживаем задачи в приложениях Django
app.autodiscover_tasks(['async_mysql_project'])

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
