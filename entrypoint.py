import os
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
    manage_py_path = os.path.abspath("async_mysql_project/manage.py")
    venv_python = os.path.join(os.getenv("VIRTUAL_ENV", ""), "Scripts", "python")
    # Проверяем наличие таблиц
    if check_tables_exist():
        print("Таблицы найдены. Пропускаем миграции.")
    else:
        print("Таблицы отсутствуют. Выполняем миграции...")
        subprocess.run([venv_python, manage_py_path, "makemigrations"], check=True)
        subprocess.run([venv_python, manage_py_path, "migrate"], check=True)

if __name__ == "__main__":
    main()
