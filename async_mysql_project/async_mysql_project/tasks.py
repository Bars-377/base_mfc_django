from celery import shared_task
from asgiref.sync import sync_to_async
import os

import pandas as pd
from io import BytesIO
from openpyxl.styles import PatternFill, Border, Side

@shared_task
def generate_excel(sid, data):
    """
    Генерация Excel-файла с данными.
    """
    try:
        from data_app.models import Services, Services_Two, Services_Three

        print('POPAL')
        exit()

        print(f"Начало экспорта для сессии {sid} с данными: {data}")

        contract_date = data.get('contract_date', None)

        end_date = data.get('end_date', None)

        query = sync_to_async(Services.objects.all, thread_sensitive=True)()

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
                query = sync_to_async(filter_func)(query)
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
        from django.db.models import IntegerField, DateField
        from django.db.models.functions import Cast

        query = query.annotate(
            id_id_int=Cast('id_id', IntegerField()),
            contract_date_date=Cast('contract_date', DateField())
        ).order_by('id_id_int', 'contract_date_date')

        services = query
        print(f"Получено {len(services)} услуг.")

        df = pd.DataFrame([{
            '№ п/п': service.id_id,
            'ФИО заявителя': service.name,
            'СНИЛС': service.snils,
            'Район': service.location,
            'Населённый пункт': service.address_p,
            'Адрес': service.address,
            'Льгота': service.benefit,
            'Серия и номер': service.number,
            'Дата выдачи сертификата': service.year,
            'Размер выплаты': service.cost,
            'Сертификат': service.certificate,
            'Дата и номер решения о выдаче': service.date_number_get,
            'Дата и № решения об аннулировании': service.date_number_cancellation,
            'Дата решения об отказе в выдаче': service.date_number_no_one,
            '№ решения об отказе в выдаче': service.date_number_no_two,
            'Отказ в выдаче': service.certificate_no,
            'Причина отказа': service.reason,
            'ТРЕК': service.track,
            'Дата отправки почтой': service.date_post,
            'Комментарий': service.comment,
            'Color': getattr(service, 'color', '')
        } for service in services])

        # Приводим колонки к числовому типу данных
        df['Размер выплаты'] = pd.to_numeric(df['Размер выплаты'], errors='coerce')
        df['Сертификат'] = pd.to_numeric(df['Сертификат'], errors='coerce')
        df['Отказ в выдаче'] = pd.to_numeric(df['Отказ в выдаче'], errors='coerce')

        # Расчет итогов
        total_cost = df['Размер выплаты'].sum()
        total_certificate = df['Сертификат'].sum()
        total_certificate_no = df['Отказ в выдаче'].sum()

        # Создание строки с итогами
        totals_row = pd.DataFrame([{
            '№ п/п': '',
            'ФИО заявителя': '',
            'СНИЛС': '',
            'Район': '',
            'Населённый пункт': '',
            'Адрес': '',
            'Льгота': '',
            'Серия и номер': '',
            'Дата выдачи сертификата': '',
            'Размер выплаты': total_cost,
            'Сертификат': total_certificate,
            'Дата и номер решения о выдаче': '',
            'Дата и № решения об аннулировании': '',
            'Дата решения об отказе в выдаче': '',
            '№ решения об отказе в выдаче': '',
            'Отказ в выдаче': total_certificate_no,
            'Причина отказа': '',
            'ТРЕК': '',
            'Дата отправки почтой': '',
            'Комментарий': '',
            'Color': ''
        }])

        # Добавление строки с итогами в DataFrame
        df = pd.concat([df, totals_row], ignore_index=True)

        # Создаем файл Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Services')

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
            for row_num in range(2, worksheet.max_row + 1):  # Пропускаем заголовки
                for col_num in range(1, worksheet.max_column + 1):
                    cell = worksheet.cell(row=row_num, column=col_num)
                    cell.border = border_style

                    # Применяем цвет только к ячейкам данных
                    color = df.iloc[row_num - 2]['Color']  # Сопоставление индексов DataFrame
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

        import datetime
        date = str(datetime.datetime.now().date())

        # Получаем текущую директорию проекта
        project_dir = os.path.dirname(os.path.abspath(__file__))

        # Строим путь к папке file внутри проекта
        file_path = os.path.join(project_dir, 'file', f'services_{sid}_{date}.xlsx')

        # Сохраняем файл на диск
        with open(file_path, 'wb') as f:
            f.write(output.read())

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
        socketio.emit('export_error', {'message': str(e)}, room=request.sid)
