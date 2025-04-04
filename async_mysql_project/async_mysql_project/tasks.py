from celery import shared_task
from asgiref.sync import async_to_sync
import os

import pandas as pd
from io import BytesIO
from openpyxl.styles import PatternFill, Border, Side
from channels.layers import get_channel_layer

@shared_task
def generate_excel(sid, data):
    """
    Генерация Excel-файла с данными.
    """
    try:
        from data_app.models import Services, Services_Two, Services_Three

        print(f"Начало экспорта для сессии {sid} с данными: {data}")

        contract_date = data[0]

        end_date = data[1]

        query = Services.objects.all()

        # Регулярное выражение для формата "DD.MM.YYYY"
        pattern_dd_mm_yyyy = r'\b\d{2}\.\d{2}\.\d{4}\b'

        # Регулярное выражение для формата "YYYY-MM-DD"
        pattern_yyyy_mm_dd = r'\b\d{4}-\d{2}-\d{2}\b'

        if contract_date == 'No':
            contract_date = None
        if end_date == 'No':
            end_date = None

        def apply_filters(query, filters):
            for filter_func in filters:
                query = filter_func(query)
            return query

        from django.db.models import Q

        filters = []
        if contract_date == 'None' and end_date == 'None':
            filters.append(lambda q: q.exclude(Q(contract_date__regex=pattern_dd_mm_yyyy) | Q(contract_date__regex=pattern_yyyy_mm_dd) | Q(end_date__regex=pattern_dd_mm_yyyy) | Q(end_date__regex=pattern_yyyy_mm_dd)))
        elif contract_date == 'None':
            filters.append(lambda q: q.exclude(Q(contract_date__regex=pattern_dd_mm_yyyy) | Q(contract_date__regex=pattern_yyyy_mm_dd)))
            if end_date:
                filters.append(lambda q: q.filter(end_date__icontains=end_date))
        elif end_date == 'None':
            filters.append(lambda q: q.exclude(Q(end_date__regex=pattern_dd_mm_yyyy) | Q(end_date__regex=pattern_yyyy_mm_dd)))
            if contract_date:
                filters.append(lambda q: q.filter(contract_date__icontains=contract_date))
        elif contract_date and end_date:
            filters.append(lambda q: q.filter(Q(contract_date__icontains=contract_date) | Q(end_date__icontains=end_date)))
        elif contract_date:
            filters.append(lambda q: q.filter(contract_date__icontains=contract_date))
        elif end_date:
            filters.append(lambda q: q.filter(end_date__icontains=end_date))

        query = apply_filters(query, filters)

        # Сортировка
        from django.db.models import IntegerField
        from django.db.models.functions import Cast

        query = query.annotate(
            id_id_int=Cast('id_id', IntegerField())
        ).order_by('id_id_int')

        services = query
        print(f"Получено {len(services)} услуг.")

        df = pd.DataFrame([{
            '№ п/п': service.id_id,
            'Наименование закупки': service.name,
            'Статус': service.status,
            'Способ закупки': service.way,
            'Инициатор закупки (ИТ/АХО)': service.initiator,
            'КЦСР': service.KTSSR,
            'КОСГУ': service.KOSGU,
            'ДопФК': service.DopFC,
            'НМЦК': service.NMCC,
            'Экономия': service.saving,
            'Контрагент': service.counterparty,
            'Реестровый номер контракта (ЕИС)': service.registration_number,
            'Номер контракта': service.contract_number,
            'Дата контракта': service.contract_date,
            'Окончание даты исполнения': service.end_date,
            'Цена контракта (на 2024 год)': service.contract_price,
            'Исполнение контракта (план) (формула)': service.execution_contract_plan,
            'Январь (план)': service.january_one,
            'Февраль (план)': service.february,
            'Март (план)': service.march,
            'Апрель (план)': service.april,
            'Май (план)': service.may,
            'Июнь (план)': service.june,
            'Июль (план)': service.july,
            'Август (план)': service.august,
            'Сентябрь (план)': service.september,
            'Октябрь (план)': service.october,
            'Ноябрь (план)': service.november,
            'Декабрь (план)': service.december,
            'Январь (план) (доп)': service.january_two,
            'Исполнение контракта (факт) (формула)': service.execution_contract_fact,
            'Дата оплаты 1': service.date_january_one,
            'Сумма оплаты 1': service.sum_january_one,
            'Дата оплаты 2': service.date_february,
            'Сумма оплаты 2': service.sum_february,
            'Дата оплаты 3': service.date_march,
            'Сумма оплаты 3': service.sum_march,
            'Дата оплаты 4': service.date_april,
            'Сумма оплаты 4': service.sum_april,
            'Дата оплаты 5': service.date_may,
            'Сумма оплаты 5': service.sum_may,
            'Дата оплаты 6': service.date_june,
            'Сумма оплаты 6': service.sum_june,
            'Дата оплаты 7': service.date_july,
            'Сумма оплаты 7': service.sum_july,
            'Дата оплаты 8': service.date_august,
            'Сумма оплаты 8': service.sum_august,
            'Дата оплаты 9': service.date_september,
            'Сумма оплаты 9': service.sum_september,
            'Дата оплаты 10': service.date_october,
            'Сумма оплаты 10': service.sum_october,
            'Дата оплаты 11': service.date_november,
            'Сумма оплаты 11': service.sum_november,
            'Дата оплаты 12': service.date_december,
            'Сумма оплаты 12': service.sum_december,
            'Дата оплаты 13': service.date_january_two,
            'Сумма оплаты 13': service.sum_january_two,
            '% исполнения (формула)': service.execution,
            'Остаток по контракту (формула)': service.contract_balance,
            'Color': getattr(service, 'color', '')
        } for service in services])

        # Приводим колонки к числовому типу данных
        df['НМЦК'] = pd.to_numeric(df['НМЦК'], errors='coerce')
        df['Цена контракта (на 2024 год)'] = pd.to_numeric(df['Цена контракта (на 2024 год)'], errors='coerce')
        df['Исполнение контракта (факт) (формула)'] = pd.to_numeric(df['Исполнение контракта (факт) (формула)'], errors='coerce')

        # Расчет итогов
        total_cost = df['НМЦК'].sum()
        total_certificate = df['Цена контракта (на 2024 год)'].sum()
        total_certificate_no = df['Исполнение контракта (факт) (формула)'].sum()

        # Создание строки с итогами
        totals_row = pd.DataFrame([{
            '№ п/п': '',
            'Наименование закупки': '',
            'Статус': '',
            'Способ закупки': '',
            'Инициатор закупки (ИТ/АХО)': '',
            'КЦСР': '',
            'КОСГУ': '',
            'ДопФК': '',
            'НМЦК': total_cost,
            'Экономия': '',
            'Контрагент': '',
            'Реестровый номер контракта (ЕИС)': '',
            'Номер контракта': '',
            'Дата контракта': '',
            'Окончание даты исполнения': '',
            'Цена контракта (на 2024 год)': total_certificate,
            'Исполнение контракта (план) (формула)': '',
            'Январь (план)': '',
            'Февраль (план)': '',
            'Март (план)': '',
            'Апрель (план)': '',
            'Май (план)': '',
            'Июнь (план)': '',
            'Июль (план)': '',
            'Август (план)': '',
            'Сентябрь (план)': '',
            'Октябрь (план)': '',
            'Ноябрь (план)': '',
            'Декабрь (план)': '',
            'Январь (план) (доп)': '',
            'Исполнение контракта (факт) (формула)': total_certificate_no,
            'Дата оплаты 1': '',
            'Сумма оплаты 1': '',
            'Дата оплаты 2': '',
            'Сумма оплаты 2': '',
            'Дата оплаты 3': '',
            'Сумма оплаты 3': '',
            'Дата оплаты 4': '',
            'Сумма оплаты 4': '',
            'Дата оплаты 5': '',
            'Сумма оплаты 5': '',
            'Дата оплаты 6': '',
            'Сумма оплаты 6': '',
            'Дата оплаты 7': '',
            'Сумма оплаты 7': '',
            'Дата оплаты 8': '',
            'Сумма оплаты 8': '',
            'Дата оплаты 9': '',
            'Сумма оплаты 9': '',
            'Дата оплаты 10': '',
            'Сумма оплаты 10': '',
            'Дата оплаты 11': '',
            'Сумма оплаты 11': '',
            'Дата оплаты 12': '',
            'Сумма оплаты 12': '',
            'Дата оплаты 13': '',
            'Сумма оплаты 13': '',
            '% исполнения (формула)': '',
            'Остаток по контракту (формула)': '',
            'Color': ''
        }])

        empty_rows_1 = pd.DataFrame([{
            '№ п/п': '№ п/п',
            'Наименование закупки': 'Наименование закупки',
            'Статус': 'Статус',
            'Способ закупки': 'Способ закупки',
            'Инициатор закупки (ИТ/АХО)': 'Инициатор закупки (ИТ/АХО)',
            'КЦСР': 'КЦСР',
            'КОСГУ': 'КОСГУ',
            'ДопФК': 'ДопФК',
            'НМЦК': 'НМЦК',
            'Экономия': 'Экономия',
            'Контрагент': 'Контрагент',
            'Реестровый номер контракта (ЕИС)': 'Реестровый номер контракта (ЕИС)',
            'Номер контракта': 'Номер контракта',
            'Дата контракта': 'Дата контракта',
            'Окончание даты исполнения': 'Окончание даты исполнения',
            'Цена контракта (на 2024 год)': 'Цена контракта (на 2024 год)',
            'Исполнение контракта (план) (формула)': 'Исполнение контракта (план) (формула)',
            'Январь (план)': 'Январь (план)',
            'Февраль (план)': 'Февраль (план)',
            'Март (план)': 'Март (план)',
            'Апрель (план)': 'Апрель (план)',
            'Май (план)': 'Май (план)',
            'Июнь (план)': 'Июнь (план)',
            'Июль (план)': 'Июль (план)',
            'Август (план)': 'Август (план)',
            'Сентябрь (план)': 'Сентябрь (план)',
            'Октябрь (план)': 'Октябрь (план)',
            'Ноябрь (план)': 'Ноябрь (план)',
            'Декабрь (план)': 'Декабрь (план)',
            'Январь (план) (доп)': 'Январь (план) (доп)',
            'Исполнение контракта (факт) (формула)': 'Исполнение контракта (факт) (формула)',
            'Дата оплаты 1':'Дата оплаты 1',
            'Сумма оплаты 1': 'Сумма оплаты 1',
            'Дата оплаты 2': 'Дата оплаты 2',
            'Сумма оплаты 2': 'Сумма оплаты 2',
            'Дата оплаты 3': 'Дата оплаты 3',
            'Сумма оплаты 3': 'Сумма оплаты 3',
            'Дата оплаты 4': 'Дата оплаты 4',
            'Сумма оплаты 4': 'Сумма оплаты 4',
            'Дата оплаты 5': 'Дата оплаты 5',
            'Сумма оплаты 5': 'Сумма оплаты 5',
            'Дата оплаты 6': 'Дата оплаты 6',
            'Сумма оплаты 6': 'Сумма оплаты 6',
            'Дата оплаты 7': 'Дата оплаты 7',
            'Сумма оплаты 7': 'Сумма оплаты 7',
            'Дата оплаты 8': 'Дата оплаты 8',
            'Сумма оплаты 8': 'Сумма оплаты 8',
            'Дата оплаты 9': 'Дата оплаты 9',
            'Сумма оплаты 9': 'Сумма оплаты 9',
            'Дата оплаты 10': 'Дата оплаты 10',
            'Сумма оплаты 10': 'Сумма оплаты 10',
            'Дата оплаты 11': 'Дата оплаты 11',
            'Сумма оплаты 11': 'Сумма оплаты 11',
            'Дата оплаты 12': 'Дата оплаты 12',
            'Сумма оплаты 12': 'Сумма оплаты 12',
            'Дата оплаты 13': 'Дата оплаты 13',
            'Сумма оплаты 13': 'Сумма оплаты 13',
            '% исполнения (формула)': '% исполнения (формула)',
            'Остаток по контракту (формула)': 'Остаток по контракту (формула)',
            'Color': 'Color'
        }])

        empty_rows_2 = pd.DataFrame([{
            '№ п/п': '',
            'Наименование закупки': '',
            'Статус': '',
            'Способ закупки': '',
            'Инициатор закупки (ИТ/АХО)': '',
            'КЦСР': '',
            'КОСГУ': '',
            'ДопФК': '',
            'НМЦК': '',
            'Экономия': '',
            'Контрагент': '',
            'Реестровый номер контракта (ЕИС)': '',
            'Номер контракта': '',
            'Дата контракта': '',
            'Окончание даты исполнения': '',
            'Цена контракта (на 2024 год)': '',
            'Исполнение контракта (план) (формула)': '',
            'Январь (план)': '',
            'Февраль (план)': '',
            'Март (план)': '',
            'Апрель (план)': '',
            'Май (план)': '',
            'Июнь (план)': '',
            'Июль (план)': '',
            'Август (план)': '',
            'Сентябрь (план)': '',
            'Октябрь (план)': '',
            'Ноябрь (план)': '',
            'Декабрь (план)': '',
            'Январь (план) (доп)': '',
            'Исполнение контракта (факт) (формула)': '',
            'Дата оплаты 1':'Дата оплаты 1',
            'Сумма оплаты 1': 'Сумма оплаты 1',
            'Дата оплаты 2': 'Дата оплаты 2',
            'Сумма оплаты 2': 'Сумма оплаты 2',
            'Дата оплаты 3': 'Дата оплаты 3',
            'Сумма оплаты 3': 'Сумма оплаты 3',
            'Дата оплаты 4': 'Дата оплаты 4',
            'Сумма оплаты 4': 'Сумма оплаты 4',
            'Дата оплаты 5': 'Дата оплаты 5',
            'Сумма оплаты 5': 'Сумма оплаты 5',
            'Дата оплаты 6': 'Дата оплаты 6',
            'Сумма оплаты 6': 'Сумма оплаты 6',
            'Дата оплаты 7': 'Дата оплаты 7',
            'Сумма оплаты 7': 'Сумма оплаты 7',
            'Дата оплаты 8': 'Дата оплаты 8',
            'Сумма оплаты 8': 'Сумма оплаты 8',
            'Дата оплаты 9': 'Дата оплаты 9',
            'Сумма оплаты 9': 'Сумма оплаты 9',
            'Дата оплаты 10': 'Дата оплаты 10',
            'Сумма оплаты 10': 'Сумма оплаты 10',
            'Дата оплаты 11': 'Дата оплаты 11',
            'Сумма оплаты 11': 'Сумма оплаты 11',
            'Дата оплаты 12': 'Дата оплаты 12',
            'Сумма оплаты 12': 'Сумма оплаты 12',
            'Дата оплаты 13': 'Дата оплаты 13',
            'Сумма оплаты 13': 'Сумма оплаты 13',
            '% исполнения (формула)': '',
            'Остаток по контракту (формула)': '',
            'Color': 'Color'
        }])

        # print('-----------------------')
        # print(f"Первое {empty_rows_1.columns}")
        # print(f"Первое {empty_rows_2.columns}")
        # print(f"Второе {df.columns}")
        # print(f"Третье {totals_row.columns}")

        # exit()

        # # Перемещаем все DataFrame в одну структуру с одинаковыми столбцами
        # empty_rows_1 = empty_rows_1[columns]
        # empty_rows_2 = empty_rows_2[columns]
        # df = df[columns]
        # totals_row = totals_row[columns]

        # Добавление строки с итогами в DataFrame
        df = pd.concat([empty_rows_1, empty_rows_2, df, totals_row], ignore_index=True)
        # df = pd.concat([df, totals_row], ignore_index=True)

        # Создаем файл Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, header=False, sheet_name='Services', startcol=0)

            # Настройка стиля
            worksheet = writer.sheets['Services']

            # Определяем стиль для границ
            border_style = Border(left=Side(style='thin'),
                                right=Side(style='thin'),
                                top=Side(style='thin'),
                                bottom=Side(style='thin'))

            # Определяем стиль для заливки желтым цветом
            yellow_fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')

            import re
            def is_valid_hex_color(color):
                # Регулярное выражение для проверки формата цвета
                pattern = r'^#[0-9A-Fa-f]{6}$'
                return bool(re.match(pattern, color))

            # Применяем границы ко всем ячейкам и цвет к ячейкам, где он задан
            for row_num in range(2, worksheet.max_row):  # Пропускаем заголовки
                for col_num in range(1, worksheet.max_column + 1):
                    cell = worksheet.cell(row=row_num + 1, column=col_num)
                    cell.border = border_style

                    # Применяем цвет только к ячейкам данных
                    color = df.iloc[row_num]['Color']  # Сопоставление индексов DataFrame
                    # print('POPAL_HA', f"Один {color}", f"Два {type(color)}")
                    # exit()
                    if color and is_valid_hex_color(color):
                        cell.fill = PatternFill(start_color=color.replace('#', ''), end_color=color.replace('#', ''), fill_type="solid")

            # Применяем границы к заголовкам
            for col_num in range(1, worksheet.max_column + 1):
                cell = worksheet.cell(row=1, column=col_num)
                cell.border = border_style

            # Применяем желтый цвет к строке с итогами
            totals_row_num = worksheet.max_row
            for col_num in range(1, worksheet.max_column + 1):
                cell = worksheet.cell(row=totals_row_num, column=col_num)
                cell.fill = yellow_fill
                cell.border = border_style

            # Удаляем столбец Color из Excel-файла
            worksheet.delete_cols(df.columns.get_loc("Color") + 1)

        output.seek(0)

        from openpyxl import load_workbook
        from openpyxl.styles import Alignment

        import datetime
        date = str(datetime.datetime.now().date())

        # Получаем текущую директорию проекта
        project_dir = os.path.dirname(os.path.abspath(__file__))

        # Строим путь к папке file внутри проекта
        file_path = os.path.join(project_dir, 'file', f'services_{sid}_{date}.xlsx')

        # Сохраняем файл на диск
        with open(file_path, 'wb') as f:
            f.write(output.read())

        # print('POPAL FILE', project_dir)
        # exit()

        # Открытие файла с openpyxl для объединения ячеек
        wb = load_workbook(file_path)
        ws = wb.active

        # Объединение ячеек (пример для первых 7 колонок)
        for col in range(1, 60):  # 1 - это 'A', 2 - это 'B' и т.д.
            if 32 <= col <= 57 and col % 2 == 0: # Исключаем 33, 35, 37 и т.д.
                ws.merge_cells(start_row=1, start_column=col, end_row=1, end_column=col+1)
            elif not (32 <= col <= 57):
                ws.merge_cells(start_row=1, start_column=col, end_row=2, end_column=col)

        # Выравниваем текст по центру
        for row in ws.iter_rows(min_row=1, max_row=2, min_col=1, max_col=59):
            for cell in row:
                cell.alignment = Alignment(horizontal="center", vertical="center")

        # Сохранение изменений
        wb.save(file_path)

        # Возвращаем путь к файлу для отправки клиенту
        filename = f"services_{sid}_{date}.xlsx"
        file_url = f"/file/{filename}"

        # # Emit the success event with file URL
        # socketio.emit('export_success', {'file_url': file_url, 'filename': filename}, room=sid)

        return file_url, filename

        # # Преобразуем файл в base64, чтобы отправить его через WebSocket
        # file_data = base64.b64encode(output.read()).decode('utf-8')
        # # return file_data

        # print(f"Отправка данных клиенту: {file_data}, имя файла: services.xlsx")

        # return file_data

    except Exception as e:
        print(f"Ошибка в задаче для сессии {sid}: {e}")
        # Работа с channel_layer через sync_to_async
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "export_error",
            {
                "type": "export.error",
                "message": str(e),
            }
        )
