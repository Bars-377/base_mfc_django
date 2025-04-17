import time
import threading
import subprocess

def run_command(command, cwd=None):
    subprocess.run(command, cwd=cwd)

if __name__ == "__main__":

    # Укажите путь к директории, в которой нужно запустить t1
    async_mysql_project_dir = r"./async_mysql_project" # для Docker

    venv_python = "python"  # для Docker

    t1 = threading.Thread(target=run_command, args=(["uvicorn", "async_mysql_project.asgi:application", "--host", "0.0.0.0", "--port", "8400"], async_mysql_project_dir))
    t1.start()
    time.sleep(2)

    t2 = threading.Thread(target=run_command, args=([venv_python, "backup_base.py"], async_mysql_project_dir))
    t2.start()

    # ожидание завершения всех потоков
    t1.join()
    t2.join()