# Инструкция

## Настройка

1. Открыть nginx.conf по пути \nginx-1.27.1\conf

   Изменить в location proxy_pass на свой ip
2. Открыть pyvenv.cfg по пути \venv

   Изменить пути к интерпритаторам

## Запуск

1. Создать виртуальное окружение:
         python -m venv venv_home

2. Запустить виртуальное окружение:

         .\venv\Scripts\activate

3. Затем сделайте миграции:

   Зайти в дирректорию async_mysql_project

         python manage.py makemigrations

         python manage.py migrate

4. Запустить приложение:

   Зайти в дирректорию async_mysql_project

         uvicorn async_mysql_project.asgi:application --host 127.0.0.1 --port 8500

## Дополнительно:

Создаёт requirements.txt:

      python -m pip freeze > requirements.txt

Установить requirements.txt:

      python -m pip install -r requirements.txt

   PowerShell

   python -m pip freeze | ForEach-Object { python -m pip uninstall -y $_ }

## Celery:

   Запуск воркера:

      python -m celery -A app:celery worker --loglevel=INFO --pool=solo

   Запуск фловера:

      python -m celery -A app:celery flower