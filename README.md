# Инструкция

## Демонстрация
![alt text](procurement.gif)

## Запуск

1. Создать виртуальное окружение:

         python -m venv venv

2. Запустить виртуальное окружение:

         .\venv\Scripts\activate

3. Затем сделайте миграции:

   Зайти в дирректорию async_mysql_project

         python manage.py makemigrations

         python manage.py migrate

4. Запустить приложение:

   Стандартный запуск:

         python start_default.py

## Дополнительно:

Создаёт requirements.txt:

      python -m pip freeze > requirements.txt

Установить requirements.txt:

      python -m pip install -r requirements.txt

PowerShell:

      python -m pip freeze | ForEach-Object { python -m pip uninstall -y $_ }
