import pandas as pd
from django.db import DataError
from django.http import JsonResponse
import asyncio
from .views import ContractProcessor, log_user_action, clean_number

import os
import json
project_dir = os.path.dirname(os.path.abspath(__file__))
folder_path = os.path.join(project_dir, '..', '..')
folder_path = os.path.abspath(folder_path)
# Открываем файл и загружаем данные
with open(f'{folder_path}//general_settings.json', 'r', encoding='utf-8-sig') as file:
    json_object = json.load(file)

async def upload_file_(request):
    if request.method == "POST" and request.FILES.get("file"):
        uploaded_file = request.FILES["file"]

        # Если файл .xlsx, можно использовать pandas для обработки
        if uploaded_file.name.endswith('.xlsx'):
            # Чтение файла с помощью pandas
            try:
                df = pd.read_excel(uploaded_file, header=None, dtype=str)

                # Получаем количество столбцов
                num_columns = df.shape[1]
                if num_columns == 59:
                    # Здесь вы можете работать с DataFrame df
                    import mysql.connector
                    import re
                    from datetime import datetime

                    # # Установите соединение с базой данных
                    # conn = mysql.connector.connect(
                    #     # host='172.18.11.104',
                    #     host='localhost',
                    #     user='root',        # Замените на ваше имя пользователя
                    #     password='enigma1418',    # Замените на ваш пароль
                    #     database='basemfcdjango'
                    # )
                    # cursor = conn.cursor()

                    async def clean_string(input_string):
                        """
                        Очищает строку, удаляя символы новой строки (\n),
                        заменяя двойные пробелы на одинарные и удаляя пробелы в начале и конце строки.

                        Args:
                            input_string (str): Строка для очистки.

                        Returns:
                            str: Очищенная строка.
                        """

                        input_string = str(input_string)

                        # Удаляем символы новой строки
                        string_without_newlines = input_string.replace('\n', '')

                        # Заменяем двойные пробелы на одинарные
                        string_single_spaces = string_without_newlines.replace('  ', ' ')

                        #Удаляем повторяющиеся пробелы, пока они не исчезнут
                        while '  ' in string_single_spaces:
                            string_single_spaces = string_single_spaces.replace('  ', ' ')


                        # Удаляем пробелы в начале и конце строки
                        cleaned_string = string_single_spaces.strip()

                        return cleaned_string

                    # Столбцы, в которые нужно вставить данные
                    columns_to_fill = [32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56]
                    columns_to_fill_ = [31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55]

                    # Заполняем значения в первой строке данными из второй строки
                    for col in columns_to_fill:
                        df.iloc[0, col] = df.iloc[1, col]

                    # Применяем функцию clean_string ко всем именам столбцов
                    for col in range(df.shape[1]):
                        df.iloc[0, col] = await clean_string(df.iloc[0, col])

                    for col in columns_to_fill_:
                        df.iloc[0, col] = await clean_string(df.iloc[1, col])

                    df.iloc[0, 29] = 'Январь (план один)' + ' ' + await clean_string(df.iloc[0, 31])

                    df.iloc[0, 31] = 'Январь (факт 1)' + ' ' + await clean_string(df.iloc[0, 31])
                    df.iloc[0, 33] = 'Февраль (факт)' + ' ' + await clean_string(df.iloc[0, 33])
                    df.iloc[0, 35] = 'Март (факт)' + ' ' + await clean_string(df.iloc[0, 35])
                    df.iloc[0, 37] = 'Апрель (факт)' + ' ' + await clean_string(df.iloc[0, 37])
                    df.iloc[0, 39] = 'Май (факт)' + ' ' + await clean_string(df.iloc[0, 39])
                    df.iloc[0, 41] = 'Июнь (факт)' + ' ' + await clean_string(df.iloc[0, 41])
                    df.iloc[0, 43] = 'Июль (факт)' + ' ' + await clean_string(df.iloc[0, 43])
                    df.iloc[0, 45] = 'Август (факт)' + ' ' + await clean_string(df.iloc[0, 45])
                    df.iloc[0, 47] = 'Сентябрь (факт)' + ' ' + await clean_string(df.iloc[0, 47])
                    df.iloc[0, 49] = 'Октябрь (факт)' + ' ' + await clean_string(df.iloc[0, 49])
                    df.iloc[0, 51] = 'Ноябрь (факт)' + ' ' + await clean_string(df.iloc[0, 51])
                    df.iloc[0, 53] = 'Декабрь (факт)' + ' ' + await clean_string(df.iloc[0, 53])
                    df.iloc[0, 55] = 'Январь (факт 2)' + ' ' + await clean_string(df.iloc[0, 55])

                    df.iloc[0, 32] = 'Январь (факт 1)' + ' ' + await clean_string(df.iloc[0, 32])
                    df.iloc[0, 34] = 'Февраль (факт)' + ' ' + await clean_string(df.iloc[0, 34])
                    df.iloc[0, 36] = 'Март (факт)' + ' ' + await clean_string(df.iloc[0, 36])
                    df.iloc[0, 38] = 'Апрель (факт)' + ' ' + await clean_string(df.iloc[0, 38])
                    df.iloc[0, 40] = 'Май (факт)' + ' ' + await clean_string(df.iloc[0, 40])
                    df.iloc[0, 42] = 'Июнь (факт)' + ' ' + await clean_string(df.iloc[0, 42])
                    df.iloc[0, 44] = 'Июль (факт)' + ' ' + await clean_string(df.iloc[0, 44])
                    df.iloc[0, 46] = 'Август (факт)' + ' ' + await clean_string(df.iloc[0, 46])
                    df.iloc[0, 48] = 'Сентябрь (факт)' + ' ' + await clean_string(df.iloc[0, 48])
                    df.iloc[0, 50] = 'Октябрь (факт)' + ' ' + await clean_string(df.iloc[0, 50])
                    df.iloc[0, 52] = 'Ноябрь (факт)' + ' ' + await clean_string(df.iloc[0, 52])
                    df.iloc[0, 54] = 'Декабрь (факт)' + ' ' + await clean_string(df.iloc[0, 54])
                    df.iloc[0, 56] = 'Январь (факт 2)' + ' ' + await clean_string(df.iloc[0, 56])

                    list = []

                    for col in range(df.shape[1]):
                        list.append(df.iloc[0, col])

                    # print(list)
                    # exit()

                    def convert_to_float(x):
                        # Удаляем неразрывные пробелы и другие пробелы
                        if isinstance(x, str):
                            x = x.replace('\xa0', '').strip()  # Удаляем неразрывные пробелы и обрезаем пробелы
                        try:
                            return float(x) if pd.notnull(x) and x != '' else None
                        except ValueError:
                            return 'None'  # Возвращаем None, если не удалось конвертировать

                    async def extract_number(value, default="0.00"):
                        """Извлекает первое число из строки, если оно есть."""
                        import re
                        match = re.search(r"[-+]?\d*[,\.]\d+|\d+", str(value))

                        if match:
                            number = match.group(0).replace(',', '.') # Заменяем запятую на точку
                            if number.endswith(".0"):
                                number = number[:-2] # Удаляем ".0" в конце
                            return await clean_number(number)
                            # return match.group(0).replace(',', '.')  # Заменяем запятую на точку для поддержки формата float
                        return default

                    async def extract_date_and_number(value):
                        """Извлекает дату и номер из строки."""
                        if pd.isna(value):
                            return '', ''

                        # Попробуем извлечь дату в формате ДД.ММ.ГГГГ или ГГГГ-ММ-ДД
                        date_match = re.search(r"\b(\d{2}\.\d{2}\.\d{4})\b|\b(\d{4}-\d{2}-\d{2})\b", str(value))
                        if date_match:
                            date_value = date_match.group(0)
                            remaining_value = value.replace(date_value, '').strip()  # Остальное как номер

                            try:
                                # Преобразуем строку даты в объект datetime
                                parsed_date = datetime.strptime(date_value, '%Y-%m-%d')
                                # Возвращаем дату в нужном формате
                                return parsed_date.strftime('%d.%m.%Y'), str(remaining_value).replace(' от', '').strip()
                            except ValueError:
                                return date_value, str(remaining_value).replace(' от', '').strip()

                        return '', str(value)

                    def safe_date_conversion(value):
                        """Извлекаем дату"""
                        # Если value является Series, извлекаем первое значение
                        if isinstance(value, pd.Series):
                            # Применяем конвертацию ко всем элементам Series
                            return value.apply(lambda x: convert_to_float(x))

                        elif pd.isna(value):
                            return ''  # Возвращаем None для недопустимых значений

                        # Попробуем извлечь дату в формате ДД.ММ.ГГГГ или ГГГГ-ММ-ДД
                        date_match = re.search(r"\b(\d{2}\.\d{2}\.\d{4})\b|\b(\d{4}-\d{2}-\d{2})\b", str(value))
                        if date_match:
                            date_value = date_match.group(0)

                            try:
                                # Преобразуем строку даты в объект datetime
                                parsed_date = datetime.strptime(date_value, '%Y-%m-%d')
                                # Возвращаем дату в нужном формате
                                return parsed_date.strftime('%d.%m.%Y')
                            except ValueError:
                                return date_value  # Возвращаем исходную строку, если не удаётся распарсить
                        return str(value)

                    async def safe_conversion(value):
                        """Для преобразования данных"""
                        # Если value является Series, извлекаем первое значение
                        if isinstance(value, pd.Series):
                            # Применяем конвертацию ко всем элементам Series
                            return await asyncio.gather(*[convert_to_float(x) for x in value])
                        elif pd.isna(value):
                            return ''
                        return str(value)  # Преобразуем в строку, если значение не NaN

                    async def safe_float_conversion(value):
                        # Если value является Series, извлекаем первое значение
                        if isinstance(value, pd.Series):
                            # Применяем конвертацию ко всем элементам Series
                            return value.apply(lambda x: convert_to_float(x))
                        """Для преобразолвания в float"""
                        if pd.isna(value):
                            return "0.00"
                        try:
                            number_str = await extract_number(float(value))
                            return str(float(number_str))
                        except ValueError:
                            return "0.00"

                    async def safe_int_conversion(value):
                        """Для преобразования в int"""
                        if pd.isna(value):
                            return "0.00"
                        try:
                            number_str = await extract_number(int(value))
                            return str(int(number_str))
                        except ValueError:
                            return "0.00"

                    df.columns = df.iloc[0]  # Используем первую строку как заголовки столбцов
                    df = df.drop(index=[0, 1])  # Удаляем первые две строки
                    # print(df.columns)
                    # exit()
                    # print(df.columns[df.columns.duplicated()])
                    # exit()
                    df[f'{list[0]}'] = await asyncio.gather(*[safe_conversion(val) for val in df[f'{list[0]}']])
                    df[f'{list[1]}'] = await asyncio.gather(*[safe_conversion(val) for val in df[f'{list[1]}']])
                    df[f'{list[2]}'] = await asyncio.gather(*[safe_conversion(val) for val in df[f'{list[2]}']])
                    df[f'{list[3]}'] = await asyncio.gather(*[safe_conversion(val) for val in df[f'{list[3]}']])
                    df[f'{list[4]}'] = await asyncio.gather(*[safe_conversion(val) for val in df[f'{list[4]}']])
                    df[f'{list[5]}'] = await asyncio.gather(*[safe_int_conversion(val) for val in df[f'{list[5]}']])
                    df[f'{list[6]}'] = await asyncio.gather(*[safe_int_conversion(val) for val in df[f'{list[6]}']])
                    df[f'{list[7]}'] = await asyncio.gather(*[safe_conversion(val) for val in df[f'{list[7]}']])
                    df[f'{list[8]}'] = await asyncio.gather(*[safe_float_conversion(val) for val in df[f'{list[8]}']])
                    df[f'{list[9]}'] = await asyncio.gather(*[safe_float_conversion(val) for val in df[f'{list[9]}']])
                    df[f'{list[10]}'] = await asyncio.gather(*[safe_conversion(val) for val in df[f'{list[10]}']])
                    df[f'{list[11]}'] = await asyncio.gather(*[safe_conversion(val) for val in df[f'{list[11]}']])
                    df[f'{list[12]}'] = await asyncio.gather(*[safe_conversion(val) for val in df[f'{list[12]}']])
                    df[f'{list[13]}'] = df[f'{list[13]}'].apply(safe_date_conversion)
                    df[f'{list[14]}'] = df[f'{list[14]}'].apply(safe_date_conversion)
                    df[f'{list[15]}'] = await asyncio.gather(*[safe_float_conversion(val) for val in df[f'{list[15]}']])
                    # df[f'{list[16]}'] = await asyncio.gather(*[safe_float_conversion(val) for val in df[f'{list[16]}']])
                    df[f'{list[17]}'] = await asyncio.gather(*[safe_float_conversion(val) for val in df[f'{list[17]}']])
                    df[f'{list[18]}'] = await asyncio.gather(*[safe_float_conversion(val) for val in df[f'{list[18]}']])
                    df[f'{list[19]}'] = await asyncio.gather(*[safe_float_conversion(val) for val in df[f'{list[19]}']])
                    df[f'{list[20]}'] = await asyncio.gather(*[safe_float_conversion(val) for val in df[f'{list[20]}']])
                    df[f'{list[21]}'] = await asyncio.gather(*[safe_float_conversion(val) for val in df[f'{list[21]}']])
                    df[f'{list[22]}'] = await asyncio.gather(*[safe_float_conversion(val) for val in df[f'{list[22]}']])
                    df[f'{list[23]}'] = await asyncio.gather(*[safe_float_conversion(val) for val in df[f'{list[23]}']])
                    df[f'{list[24]}'] = await asyncio.gather(*[safe_float_conversion(val) for val in df[f'{list[24]}']])
                    df[f'{list[25]}'] = await asyncio.gather(*[safe_float_conversion(val) for val in df[f'{list[25]}']])
                    df[f'{list[26]}'] = await asyncio.gather(*[safe_float_conversion(val) for val in df[f'{list[26]}']])
                    df[f'{list[27]}'] = await asyncio.gather(*[safe_float_conversion(val) for val in df[f'{list[27]}']])
                    df[f'{list[28]}'] = await asyncio.gather(*[safe_float_conversion(val) for val in df[f'{list[28]}']])
                    df[f'{list[29]}'] = await asyncio.gather(*[safe_float_conversion(val) for val in df[f'{list[29]}']])
                    df[f'{list[16]}'] = df[f'{list[17]}'].astype(float) + df[f'{list[18]}'].astype(float) + df[f'{list[19]}'].astype(float) + df[f'{list[20]}'].astype(float) + df[f'{list[21]}'].astype(float) + df[f'{list[22]}'].astype(float) + df[f'{list[23]}'].astype(float) + df[f'{list[24]}'].astype(float) + df[f'{list[25]}'].astype(float) + df[f'{list[26]}'].astype(float) + df[f'{list[27]}'].astype(float) + df[f'{list[28]}'].astype(float) + df[f'{list[29]}'].astype(float)
                    # df[f'{list[30]}'] = await asyncio.gather(*[safe_float_conversion(val) for val in df[f'{list[30]}']])
                    df[f'{list[31]}'] = df[f'{list[31]}'].apply(safe_date_conversion)
                    df[f'{list[32]}'] = await asyncio.gather(*[safe_float_conversion(val) for val in df[f'{list[32]}']])
                    df[f'{list[33]}'] = df[f'{list[33]}'].apply(safe_date_conversion)
                    df[f'{list[34]}'] = await asyncio.gather(*[safe_float_conversion(val) for val in df[f'{list[34]}']])
                    df[f'{list[35]}'] = df[f'{list[35]}'].apply(safe_date_conversion)
                    df[f'{list[36]}'] = await asyncio.gather(*[safe_float_conversion(val) for val in df[f'{list[36]}']])
                    df[f'{list[37]}'] = df[f'{list[37]}'].apply(safe_date_conversion)
                    df[f'{list[38]}'] = await asyncio.gather(*[safe_float_conversion(val) for val in df[f'{list[38]}']])
                    df[f'{list[39]}'] = df[f'{list[39]}'].apply(safe_date_conversion)
                    df[f'{list[40]}'] = await asyncio.gather(*[safe_float_conversion(val) for val in df[f'{list[40]}']])
                    df[f'{list[41]}'] = df[f'{list[41]}'].apply(safe_date_conversion)
                    df[f'{list[42]}'] = await asyncio.gather(*[safe_float_conversion(val) for val in df[f'{list[42]}']])
                    df[f'{list[43]}'] = df[f'{list[43]}'].apply(safe_date_conversion)
                    df[f'{list[44]}'] = await asyncio.gather(*[safe_float_conversion(val) for val in df[f'{list[44]}']])
                    df[f'{list[45]}'] = df[f'{list[45]}'].apply(safe_date_conversion)
                    df[f'{list[46]}'] = await asyncio.gather(*[safe_float_conversion(val) for val in df[f'{list[46]}']])
                    df[f'{list[47]}'] = df[f'{list[47]}'].apply(safe_date_conversion)
                    df[f'{list[48]}'] = await asyncio.gather(*[safe_float_conversion(val) for val in df[f'{list[48]}']])
                    df[f'{list[49]}'] = df[f'{list[49]}'].apply(safe_date_conversion)
                    df[f'{list[50]}'] = await asyncio.gather(*[safe_float_conversion(val) for val in df[f'{list[50]}']])
                    df[f'{list[51]}'] = df[f'{list[51]}'].apply(safe_date_conversion)
                    df[f'{list[52]}'] = await asyncio.gather(*[safe_float_conversion(val) for val in df[f'{list[52]}']])
                    df[f'{list[53]}'] = df[f'{list[53]}'].apply(safe_date_conversion)
                    df[f'{list[54]}'] = await asyncio.gather(*[safe_float_conversion(val) for val in df[f'{list[54]}']])
                    df[f'{list[55]}'] = df[f'{list[55]}'].apply(safe_date_conversion)
                    df[f'{list[56]}'] = await asyncio.gather(*[safe_float_conversion(val) for val in df[f'{list[56]}']])
                    df[f'{list[30]}'] = df[f'{list[32]}'].astype(float) + df[f'{list[34]}'].astype(float) + df[f'{list[36]}'].astype(float) + df[f'{list[38]}'].astype(float) + df[f'{list[40]}'].astype(float) + df[f'{list[42]}'].astype(float) + df[f'{list[44]}'].astype(float) + df[f'{list[46]}'].astype(float) + df[f'{list[48]}'].astype(float) + df[f'{list[50]}'].astype(float) + df[f'{list[52]}'].astype(float) + df[f'{list[54]}'].astype(float) + df[f'{list[56]}'].astype(float)
                    # df[f'{list[57]}'] = await asyncio.gather(*[safe_conversion(val) for val in df[f'{list[57]}']])

                    import numpy as np

                    # Преобразуем столбцы в float, используя errors='coerce' для обработки некорректных значений
                    df[f'{list[30]}'] = pd.to_numeric(df[f'{list[30]}'], errors='coerce')
                    df[f'{list[15]}'] = pd.to_numeric(df[f'{list[15]}'], errors='coerce')

                    # Используем np.where для создания нового столбца
                    df[f'{list[57]}'] = np.where(
                        df[f'{list[30]}'] != 0,  # Условие: если значение в столбце не равно 0
                        (df[f'{list[30]}'] / df[f'{list[15]}'] * 100).astype(str),  # Деление и округление
                        '0'  # Если значение равно 0, то присваиваем '0'
                    )

                    # df[f'{list[57]}'] = (round(df[f'{list[30]}'].astype(float) / df[f'{list[15]}'].astype(float), 2) * 100).astype(str)
                    # df[f'{list[58]}'] = await asyncio.gather(*[safe_float_conversion(val) for val in df[f'{list[58]}']])
                    df[f'{list[58]}'] = df[f'{list[15]}'].astype(float) - df[f'{list[30]}'].astype(float)

                    # Определите SQL-запрос для вставки данных
                    insert_query = """
                    INSERT INTO services (
                        id_id, name, status, way, initiator, KTSSR, KOSGU, DopFC, NMCC, saving,
                        counterparty, registration_number, contract_number, contract_date, end_date,
                        contract_price, execution_contract_plan, january_one, february, march, april,
                        may, june, july, august, september, october, november, december, january_two, execution_contract_fact, date_january_one,
                        sum_january_one, date_february, sum_february, date_march, sum_march, date_april, sum_april, date_may, sum_may, date_june,
                        sum_june, date_july, sum_july, date_august, sum_august, date_september, sum_september, date_october, sum_october, date_november,
                        sum_november, date_december, sum_december, date_january_two, sum_january_two, execution, contract_balance, color
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                    """

                    def validate_column(data, allowed_values, column_index, column_name, json_key, allow_empty=False):
                        """Валидирует значения столбца по допустимому списку"""
                        values = json_object['statuses'][json_key]
                        if allow_empty:
                            values.append('')

                        allowed_set = set(word.lower() for word in values)
                        for index, row in enumerate(data):
                            cell_value = str(row[column_index]).lower()
                            if cell_value not in allowed_set:
                                return JsonResponse({
                                    "message": f"Некорректная колонка {column_name} в строке таблицы Excel {index + 1}. Содержание: {cell_value}",
                                    "status": "error",
                                    'success': True
                                }, status=400)

                    # Преобразуем DataFrame в список кортежей
                    data_to_insert = [tuple(x) for x in df.to_numpy()]

                    # Валидация всех нужных колонок
                    validation_rules = [
                        {"index": 2, "name": "Статус закупки", "key": "list", "allow_empty": True},
                        {"index": 5, "name": "КЦСР закупки", "key": "KTSSR", "allow_empty": False},
                        {"index": 3, "name": "Способ закупки", "key": "purchasing_method", "allow_empty": True},
                        {"index": 6, "name": "КОСГУ закупки", "key": "KOSGU", "allow_empty": False},
                        {"index": 7, "name": "ДопФК закупки", "key": "DopFC", "allow_empty": False},
                    ]

                    for rule in validation_rules:
                        response = validate_column(
                            data_to_insert,
                            json_object['statuses'][rule['key']],
                            rule['index'],
                            rule['name'],
                            rule['key'],
                            allow_empty=rule['allow_empty']
                        )
                        if response:
                            return response

                    context_data = [{
                        'name': row[1].lower() if isinstance(row[1], str) else row[1],
                        'status': row[2].lower() if isinstance(row[2], str) else row[2],
                        'way': row[3].lower() if isinstance(row[3], str) else row[3],
                        'initiator': row[4].lower() if isinstance(row[4], str) else row[4],
                        'KTSSR': row[5].lower() if isinstance(row[5], str) else row[5],
                        'KOSGU': row[6].lower() if isinstance(row[6], str) else row[6],
                        'DopFC': row[7].lower() if isinstance(row[7], str) else row[7],
                        'NMCC': row[8].lower() if isinstance(row[8], str) else row[8],
                        'saving': row[9].lower() if isinstance(row[9], str) else row[9],
                        'counterparty': row[10].lower() if isinstance(row[10], str) else row[10],
                        'registration_number': row[11].lower() if isinstance(row[11], str) else row[11],
                        'contract_number': row[12].lower() if isinstance(row[12], str) else row[12],
                        'contract_date': row[13].lower() if isinstance(row[13], str) else row[13],
                        'end_date': row[14].lower() if isinstance(row[14], str) else row[14],
                        'contract_price': row[15].lower() if isinstance(row[15], str) else row[15],
                        # 'execution_contract_plan': row[57].lower() if isinstance(row[57], str) else row[57],
                        'january_one': row[17].lower() if isinstance(row[17], str) else row[17],
                        'february': row[18].lower() if isinstance(row[18], str) else row[18],
                        'march': row[19].lower() if isinstance(row[19], str) else row[19],
                        'april': row[20].lower() if isinstance(row[20], str) else row[20],
                        'may': row[21].lower() if isinstance(row[21], str) else row[21],
                        'june': row[22].lower() if isinstance(row[22], str) else row[22],
                        'july': row[23].lower() if isinstance(row[23], str) else row[23],
                        'august': row[24].lower() if isinstance(row[24], str) else row[24],
                        'september': row[25].lower() if isinstance(row[25], str) else row[25],
                        'october': row[26].lower() if isinstance(row[26], str) else row[26],
                        'november': row[27].lower() if isinstance(row[27], str) else row[27],
                        'december': row[28].lower() if isinstance(row[28], str) else row[28],
                        'january_two': row[29].lower() if isinstance(row[29], str) else row[29],
                        # 'execution_contract_fact': row[56].lower() if isinstance(row[56], str) else row[56],
                        'date_january_one': row[31].lower() if isinstance(row[31], str) else row[31],
                        'sum_january_one': row[32].lower() if isinstance(row[32], str) else row[32],
                        'date_february': row[33].lower() if isinstance(row[33], str) else row[33],
                        'sum_february': row[34].lower() if isinstance(row[34], str) else row[34],
                        'date_march': row[35].lower() if isinstance(row[35], str) else row[35],
                        'sum_march':  row[36].lower() if isinstance(row[36], str) else row[36],
                        'date_april': row[37].lower() if isinstance(row[37], str) else row[37],
                        'sum_april': row[38].lower() if isinstance(row[38], str) else row[38],
                        'date_may': row[39].lower() if isinstance(row[39], str) else row[39],
                        'sum_may': row[40].lower() if isinstance(row[40], str) else row[40],
                        'date_june': row[41].lower() if isinstance(row[41], str) else row[41],
                        'sum_june': row[42].lower() if isinstance(row[42], str) else row[42],
                        'date_july': row[43].lower() if isinstance(row[43], str) else row[43],
                        'sum_july': row[44].lower() if isinstance(row[44], str) else row[44],
                        'date_august': row[45].lower() if isinstance(row[45], str) else row[45],
                        'sum_august': row[46].lower() if isinstance(row[46], str) else row[46],
                        'date_september': row[47].lower() if isinstance(row[47], str) else row[47],
                        'sum_september': row[48].lower() if isinstance(row[48], str) else row[48],
                        'date_october': row[49].lower() if isinstance(row[49], str) else row[49],
                        'sum_october': row[50].lower() if isinstance(row[50], str) else row[50],
                        'date_november': row[51].lower() if isinstance(row[51], str) else row[51],
                        'sum_november': row[52].lower() if isinstance(row[52], str) else row[52],
                        'date_december': row[53].lower() if isinstance(row[53], str) else row[53],
                        'sum_december': row[54].lower() if isinstance(row[54], str) else row[54],
                        'date_january_two': row[55].lower() if isinstance(row[55], str) else row[55],
                        'sum_january_two': row[56].lower() if isinstance(row[56], str) else row[56]
                        # 'execution': row[54].lower() if isinstance(row[54], str) else row[54],
                        # 'contract_balance': row[55].lower() if isinstance(row[55], str) else row[55],
                    } for row in data_to_insert]

                    # names = [row[1].lower() for row in data_to_insert]
                    # seen_names = {}
                    # for index, name in enumerate(names):
                    #     if name in seen_names:
                    #         return JsonResponse({
                    #             "message": f"Повторяющаяся закупка '{name}' найдено в строке таблицы {index + 1}!",
                    #             "status": "error",
                    #             'success': True
                    #         }, status=400)
                    #     seen_names[name] = index  # Сохраняем индекс первого появления имени

                    def is_duplicate(t, name):
                        # Проверяем, что все три значения совпадают (имя, номер контракта и дата контракта)
                        name_match = (
                            (t[1].lower() if isinstance(t[1], str) else t[1]) == (name['name'].lower() if isinstance(name['name'], str) else name['name'])
                        )
                        contract_number_match = (
                            (t[12].lower() if isinstance(t[12], str) else t[12]) == (name['contract_number'].lower() if isinstance(name['contract_number'], str) else name['contract_number'])
                        )
                        contract_date_match = (
                            (t[13].lower() if isinstance(t[13], str) else t[13]) == (name['contract_date'].lower() if isinstance(name['contract_date'], str) else name['contract_date'])
                        )

                        return name_match and contract_number_match and contract_date_match

                    for index, name in enumerate(context_data):
                        processor = ContractProcessor(context_data)
                        if not await processor.validate_Services():
                            # Удаление первого кортежа, который соответствует условиям
                            data_to_insert = [t for t in data_to_insert if not is_duplicate(t, name)]

                            if not data_to_insert:
                                return JsonResponse({
                                    "message": "Эти закупки уже есть в базе!",
                                    "status": "error",
                                    'success': True
                                }, status=400)

                    # Преобразование всех значений в строки и добавление пустой строки в конец каждого кортежа
                    data_to_insert = [
                        tuple(str(value) if value is not None else '' for value in row) + ('',)
                        for row in data_to_insert
                    ]

                    from django.db import connection

                    if data_to_insert:
                        # Вставьте данные в базу данных
                        from asgiref.sync import sync_to_async
                        from django.db import connection

                        # Функция для выполнения синхронной операции с базой данных
                        @sync_to_async
                        def insert_data(insert_query, data_to_insert):
                            if data_to_insert:
                                with connection.cursor() as cursor:
                                    cursor.executemany(insert_query, data_to_insert)

                        await insert_data(insert_query, data_to_insert)

                        await log_user_action(request.user, f'Загрузил данные из Excel в "Закупки"')

                        processor = ContractProcessor(request)
                        await processor.count_dates()

                        # cursor.executemany(insert_query, data_to_insert)
                        # conn.commit()
                        return JsonResponse({"message": f"Данные из файла {uploaded_file.name} успешно загружены!", "status": "success", 'success': True})
                    else:
                        return JsonResponse({"message": f"Ошибка при обработке файла: Данные не загружены", "status": "error", 'success': True}, status=400)

                    # # Сохранение файла в папку file/
                    # file_instance = UploadedFile(file=uploaded_file)
                    # file_instance.save()
                else:
                    return JsonResponse({"message": "Нет соответствия количества столбцов", "status": "error", 'success': True}, status=400)
            except DataError:
                return JsonResponse({"message": "Слишком много символов в какой-то колонке", "status": "error", 'success': True}, status=400)

            except Exception as e:
                # Вывод подробной информации об ошибке
                print(f"Поймано исключение: {type(e).__name__}")
                print(f"Сообщение об ошибке: {str(e)}")
                import traceback
                print("Трассировка стека (stack trace):")
                traceback.print_exc()
                return JsonResponse({"message": "Попробуйте пересохранить данный файл", "status": "error", 'success': True}, status=400)
        else:
            return JsonResponse({"message": "Только файлы .xlsx разрешены", "status": "error", 'success': True}, status=400)

    return JsonResponse({"message": "Ошибка загрузки файла", 'success': True}, status=400)