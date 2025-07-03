# import schedule
# import time
# import django
# import os

# # Убедитесь, что Django настроен
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'async_mysql_project.async_mysql_project.settings')
# django.setup()

# from async_mysql_project.data_app.models import Services, Services_backup_one, Services_backup_two

# def backup_to_backup_one():
#     services = Services.objects.all()
#     for service in services:
#         Services_backup_one.objects.create(
#             id_id=service.id_id,
#             name=service.name,
#             status=service.status,
#             way=service.way,
#             initiator=service.initiator,
#             KTSSR=service.KTSSR,
#             KOSGU=service.KOSGU,
#             DopFC=service.DopFC,
#             NMCC=service.NMCC,
#             saving=service.saving,
#             counterparty=service.counterparty,
#             registration_number=service.registration_number,
#             contract_number=service.contract_number,
#             contract_date=service.contract_date,
#             end_date=service.end_date,
#             contract_price=service.contract_price,
#             execution_contract_plan=service.execution_contract_plan,
#             january_one=service.january_one,
#             february=service.february,
#             march=service.march,
#             april=service.april,
#             may=service.may,
#             june=service.june,
#             july=service.july,
#             august=service.august,
#             september=service.september,
#             october=service.october,
#             november=service.november,
#             december=service.december,
#             january_two=service.january_two,
#             execution_contract_fact=service.execution_contract_fact,
#             date_january_one=service.date_january_one,
#             sum_january_one=service.sum_january_one,
#             date_february=service.date_february,
#             sum_february=service.sum_february,
#             date_march=service.date_march,
#             sum_march=service.sum_march,
#             date_april=service.date_april,
#             sum_april=service.sum_april,
#             date_may=service.date_may,
#             sum_may=service.sum_may,
#             date_june=service.date_june,
#             sum_june=service.sum_june,
#             date_july=service.date_july,
#             sum_july=service.sum_july,
#             date_august=service.date_august,
#             sum_august=service.sum_august,
#             date_september=service.date_september,
#             sum_september=service.sum_september,
#             date_october=service.date_october,
#             sum_october=service.sum_october,
#             date_november=service.date_november,
#             sum_november=service.sum_november,
#             date_december=service.date_december,
#             sum_december=service.sum_december,
#             date_january_two=service.date_january_two,
#             sum_january_two=service.sum_january_two,
#             execution=service.execution,
#             contract_balance=service.contract_balance,
#             color=service.color,
#         )
#     print("Резервное копирование в Services_backup_one завершено")

# def backup_to_backup_two():
#     services = Services.objects.all()
#     for service in services:
#         Services_backup_two.objects.create(
#             id_id=service.id_id,
#             name=service.name,
#             status=service.status,
#             way=service.way,
#             initiator=service.initiator,
#             KTSSR=service.KTSSR,
#             KOSGU=service.KOSGU,
#             DopFC=service.DopFC,
#             NMCC=service.NMCC,
#             saving=service.saving,
#             counterparty=service.counterparty,
#             registration_number=service.registration_number,
#             contract_number=service.contract_number,
#             contract_date=service.contract_date,
#             end_date=service.end_date,
#             contract_price=service.contract_price,
#             execution_contract_plan=service.execution_contract_plan,
#             january_one=service.january_one,
#             february=service.february,
#             march=service.march,
#             april=service.april,
#             may=service.may,
#             june=service.june,
#             july=service.july,
#             august=service.august,
#             september=service.september,
#             october=service.october,
#             november=service.november,
#             december=service.december,
#             january_two=service.january_two,
#             execution_contract_fact=service.execution_contract_fact,
#             date_january_one=service.date_january_one,
#             sum_january_one=service.sum_january_one,
#             date_february=service.date_february,
#             sum_february=service.sum_february,
#             date_march=service.date_march,
#             sum_march=service.sum_march,
#             date_april=service.date_april,
#             sum_april=service.sum_april,
#             date_may=service.date_may,
#             sum_may=service.sum_may,
#             date_june=service.date_june,
#             sum_june=service.sum_june,
#             date_july=service.date_july,
#             sum_july=service.sum_july,
#             date_august=service.date_august,
#             sum_august=service.sum_august,
#             date_september=service.date_september,
#             sum_september=service.sum_september,
#             date_october=service.date_october,
#             sum_october=service.sum_october,
#             date_november=service.date_november,
#             sum_november=service.sum_november,
#             date_december=service.date_december,
#             sum_december=service.sum_december,
#             date_january_two=service.date_january_two,
#             sum_january_two=service.sum_january_two,
#             execution=service.execution,
#             contract_balance=service.contract_balance,
#             color=service.color,
#         )
#     print("Резервное копирование в Services_backup_two завершено")

# if __name__ == '__main__':
#     # Вторник (Tuesday)
#     schedule.every().tuesday.at("10:00").do(backup_to_backup_one)

#     # Пятница (Friday)
#     schedule.every().friday.at("10:00").do(backup_to_backup_two)

#     # Пятница (Friday)
#     schedule.every().wednesday.at("09:40").do(backup_to_backup_two)

#     print("backup_base.py запущен!")

#     while True:
#         schedule.run_pending()
#         time.sleep(60)

# import schedule
# import time
# import django
# import os
# import sys

# # Добавляем путь к проекту (если запускается не из корня)
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(BASE_DIR)

# # Настройка Django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'async_mysql_project.settings')
# django.setup()

# from data_app.models import Services, Services_backup_one, Services_backup_two

# def copy_service_to_model(service, backup_model):
#     fields = {f.name: getattr(service, f.name) for f in service._meta.fields if f.name != 'id'}
#     # Удаляем все записи в таблице backup_model (синхронно)
#     backup_model.objects.all().delete()
#     backup_model.objects.create(**fields)

# def backup_to_backup_one():
#     services = Services.objects.all()
#     for service in services:
#         copy_service_to_model(service, Services_backup_one)
#     print("✅ Резервное копирование в Services_backup_one завершено!")

# def backup_to_backup_two():
#     services = Services.objects.all()
#     for service in services:
#         copy_service_to_model(service, Services_backup_two)
#     print("✅ Резервное копирование в Services_backup_two завершено!")

# if __name__ == '__main__':
#     # Планирование задач
#     schedule.every().tuesday.at("07:00").do(backup_to_backup_one)
#     # schedule.every().wednesday.at("10:08").do(backup_to_backup_two)
#     schedule.every().thursday.at("07:00").do(backup_to_backup_two)

#     print("🚀 backup_base.py запущен!")

#     while True:
#         # print(f"Текущее время: {time.strftime('%H:%M:%S')}")
#         schedule.run_pending()
#         time.sleep(15)

import django
import os
import sys
import time
from datetime import datetime

# Добавляем путь к проекту (если запускается не из корня)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'async_mysql_project.settings')
django.setup()

from data_app.models import Services, Services_backup_one, Services_backup_two
from django.db import connection, OperationalError

def copy_service_to_model(service, backup_model):
    fields = {f.name: getattr(service, f.name) for f in service._meta.fields if f.name != 'id'}
    backup_model.objects.create(**fields)

def backup_to_backup_one():
    try:
        connection.close()  # Закрываем старое соединение, если оно "зависло"
        print("🔄 Начинаем копирование в Services_backup_one...")
        services = Services.objects.all()
        Services_backup_one.objects.all().delete()
        for service in services:
            copy_service_to_model(service, Services_backup_one)
        print("✅ Резервное копирование в Services_backup_one завершено!")
    except OperationalError as e:
        print(f"❌ Ошибка при копировании в backup_one: {e}")
    finally:
        connection.close()

def backup_to_backup_two():
    try:
        connection.close()  # Закрываем старое соединение, если оно "зависло"
        print("🔄 Начинаем копирование в Services_backup_two...")
        services = Services.objects.all()
        Services_backup_two.objects.all().delete()
        for service in services:
            copy_service_to_model(service, Services_backup_two)
        print("✅ Резервное копирование в Services_backup_two завершено!")
    except OperationalError as e:
        print(f"❌ Ошибка при копировании в backup_two: {e}")
    finally:
        connection.close()

if __name__ == '__main__':
    print("🚀 backup_base.py запущен!")

    while True:
        now = datetime.now()
        current_time = now.strftime('%A %H:%M')  # Пример: 'Tuesday 07:00'

        try:
            if current_time == "Tuesday 07:00":
            # if current_time == "Monday 09:15":
                backup_to_backup_one()
                time.sleep(60)
            elif current_time == "Thursday 07:00":
            # elif current_time == "Monday 09:16":
                backup_to_backup_two()
                time.sleep(60)
        except Exception as e:
            print(f"❌ Необработанная ошибка в основном цикле: {e}")
        finally:
            connection.close()  # Чистим соединение, даже если ничего не делали

        time.sleep(15)