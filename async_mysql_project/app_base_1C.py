import mysql.connector
from datetime import datetime
import os
import re

import json
project_dir = os.path.dirname(os.path.abspath(__file__))
folder_path = os.path.join(project_dir)
folder_path = os.path.abspath(folder_path)
# Переходим на одну категорию назад
folder_path = os.path.dirname(folder_path)
# print(folder_path)
# exit()
# Открываем файл и загружаем данные
with open(f'{folder_path}//general_settings.json', 'r', encoding='utf-8-sig') as file:
    json_object = json.load(file)

# Подключение к базе данных
conn = mysql.connector.connect(
    host=json_object['host'],
    user='root',
    password='enigma1418',
    database='mdtomskbot'
)

cursor = conn.cursor(dictionary=True)

# SQL-запрос к таблице
cursor.execute("SELECT `date`, `sum`, `agreement`, `counterparty` FROM base_1C")

rows = cursor.fetchall()

result = []

for row in rows:
    try:
        # Обработка даты: из '11.01.2023 23:59:59' в datetime
        date_str = row['date']
        date_obj = datetime.strptime(date_str.strip(), '%d.%m.%Y %H:%M:%S')

        # Обработка суммы: '37 075,31' -> 37075.31
        sum_str = row['sum']
        sum_str = sum_str.replace('\xa0', '')  # Удаление неразрывных пробелов
        sum_str = sum_str.replace(' ', '')     # Удаление обычных пробелов
        sum_str = sum_str.replace(',', '.')    # Замена запятой на точку
        sum_float = float(sum_str)

        counterparty = row['counterparty']
        agreement = row['agreement']

        # Поиск даты в agreement
        match = re.search(r'(\d{2}\.\d{2}\.\d{4})', agreement)
        if match:
            document_date_str = match.group(1)
            document_date = datetime.strptime(document_date_str, '%d.%m.%Y').date()
            document = re.sub(r' от \d{2}\.\d{2}\.\d{4}', '', agreement).strip()
        else:
            document_date = None
            document = agreement

        result.append({
            'date': date_obj,
            'sum': sum_float,
            'counterparty': counterparty,
            'document': document,
            'document_date': document_date
        })
    except Exception as e:
        print(f"Ошибка при обработке строки {row}: {e}")

# Закрытие соединения
cursor.close()
conn.close()

# Вывод результатов
for item in result:
    print(item)

import django
import sys

# Добавляем путь к проекту (если запускается не из корня)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'async_mysql_project.settings')
django.setup()

from data_app.models import Services, Services_backup_one, Services_backup_two

