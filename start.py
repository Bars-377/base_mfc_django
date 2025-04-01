import time
import threading
import subprocess

def run_command(command, cwd=None):
    subprocess.run(command, cwd=cwd)

if __name__ == "__main__":

    # Укажите путь к директории, в которой нужно запустить t1
    async_mysql_project_dir = r".\async_mysql_project"

    venv_python = r".\myvenv\Scripts\python.exe"  # для Windows

    t1 = threading.Thread(target=run_command, args=([venv_python, "-m", "celery", "-A", "async_mysql_project.celery", "worker", "--concurrency=20", "--loglevel=INFO", "--pool=solo"], async_mysql_project_dir))
    t1.start()
    time.sleep(2)

    t2 = threading.Thread(target=run_command, args=([venv_python, "-m", "celery", "-A", "async_mysql_project.celery", "flower", "--port=6666"], async_mysql_project_dir))
    t2.start()
    time.sleep(2)

    # создание и запуск потоков для каждого процесса
    t3 = threading.Thread(target=run_command, args=([venv_python, "-m", "daphne", "-b", "0.0.0.0", "-p", "8900", "async_mysql_project.asgi:application"], async_mysql_project_dir))
    t3.start()
    time.sleep(2)

    t4 = threading.Thread(target=run_command, args=(["uvicorn", "async_mysql_project.asgi:application", "--host", "127.0.0.1", "--port", "8400"], async_mysql_project_dir))
    t4.start()
    time.sleep(2)

    # ожидание завершения всех потоков
    t1.join()
    t2.join()
    t3.join()
    t4.join()
