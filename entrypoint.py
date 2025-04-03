import os
import sys
import mysql.connector
import subprocess

def check_tables_exist():
    # Получаем параметры подключения из переменных окружения
    db_config = {
        "host": os.getenv("DB_HOST", "172.18.11.104"),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", "enigma1418"),
        "database": os.getenv("DB_NAME", "basemfcdjango"),
    }

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        # Проверяем наличие таблицы "django_migrations"
        cursor.execute("SHOW TABLES LIKE 'django_migrations';")
        exists = cursor.fetchone()
        cursor.close()
        conn.close()
        return exists is not None
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    # Проверяем наличие таблиц
    if check_tables_exist():
        print("Таблицы найдены. Пропускаем миграции.")
    else:
        print("Таблицы отсутствуют. Выполняем миграции...")
        subprocess.run(["python", "async_mysql_project/manage.py", "makemigrations"], check=True)
        subprocess.run(["python", "async_mysql_project/manage.py", "migrate"], check=True)

    # Запускаем приложение
    subprocess.run(sys.argv[1:], check=True)

if __name__ == "__main__":
    main()
