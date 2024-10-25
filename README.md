# Инструкция

## Настройка

1. Открыть nginx.conf по пути \nginx-1.27.1\conf

   Изменить в location proxy_pass на свой ip
2. Открыть pyvenv.cfg по пути \venv

   Изменить пути к интерпритаторам

## Запуск

1. Запустить виртуальное окружение:

         .\venv\Scripts\activate

2. Затем сделайте миграции:

   python manage.py makemigrations

   python manage.py migrate

3. Запустить приложение:

         uvicorn async_mysql_project.asgi:application --host 127.0.0.1 --port 8000

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