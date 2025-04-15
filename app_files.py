from multiprocessing import Process
import os
import re
from datetime import datetime
from django.conf import settings
import time

def process_1():

    # Получаем текущую директорию проекта
    project_dir = os.path.dirname(os.path.abspath(__file__))

    # Строим путь к папке file внутри проекта
    folder_path = os.path.join(project_dir, 'async_mysql_project', 'async_mysql_project', 'file')

    # Создаем директорию file, если она не существует
    os.makedirs(folder_path, exist_ok=True)

    # Получаем текущую дату
    current_date = datetime.now()  # Оставляем datetime
    current_date_str = current_date.strftime('%Y-%m-%d')  # Получаем строку текущей даты

    # Шаблон для поиска даты в формате YYYY-MM-DD
    date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')

    # Проходим по всем файлам в папке
    for filename in os.listdir(folder_path):
        match = date_pattern.search(filename)  # Ищем дату в имени файла
        if match:
            date_str = match.group()  # Получаем найденную дату
            try:
                file_date = datetime.strptime(date_str, '%Y-%m-%d')  # Преобразуем строку в datetime
                file_date_str = file_date.strftime('%Y-%m-%d')  # Получаем строку даты файла

                # Сравниваем дату файла с текущей
                if file_date < current_date and file_date_str != current_date_str:  # Удаляем только если дата файла меньше текущей и не равна текущей
                    file_path = os.path.join(folder_path, filename)
                    os.remove(file_path)  # Удаляем файл
                    print(f"Удален файл: {filename}")
            except ValueError as e:
                print(f"Ошибка при обработке файла {filename}: {e}")  # Сообщаем об ошибке

if __name__ == '__main__':
    process1 = Process(target=process_1)
    print('🚀 app_files.py запущен!')
    while True:
        if not process1.is_alive():
            process1 = Process(target=process_1)
            process1.start()
            # process1.join()
        time.sleep(15)
