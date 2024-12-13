#!/bin/sh
set -e

# Функция для проверки существования таблиц
check_tables_exist() {
    python <<EOF
import os
import mysql.connector

# Получаем параметры подключения из переменных окружения
db_config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "enigma1418"),
    "database": os.getenv("DB_NAME", "mdtomskbot"),
}

try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    # Проверяем наличие таблицы "django_migrations"
    cursor.execute("SHOW TABLES LIKE 'django_migrations';")
    exists = cursor.fetchone()
    if exists:
        print("Tables exist")
        exit(0)
    else:
        print("Tables do not exist")
        exit(1)
except Exception as e:
    print(f"Error: {e}")
    exit(1)
EOF
}

# Проверяем наличие таблиц
if check_tables_exist; then
    echo "Таблицы найдены. Пропускаем миграции."
else
    echo "Таблицы отсутствуют. Выполняем миграции..."
    python manage.py makemigrations
    python manage.py migrate
fi

# Запускаем приложение
exec "$@"
