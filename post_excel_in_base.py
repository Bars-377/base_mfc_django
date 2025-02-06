import pandas as pd
import mysql.connector
import re
from datetime import datetime

# Установите соединение с базой данных
conn = mysql.connector.connect(
    # host='172.18.11.104',
    host='localhost',
    user='root',        # Замените на ваше имя пользователя
    password='enigma1418',    # Замените на ваш пароль
    database='basemfcdjango'
)
cursor = conn.cursor()

def clean_string(input_string):
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

try:
    # Загрузите данные из Excel
    file_path = 'C:/Users/neverov/Desktop/gos.xlsx'
    sheet_name = 'ЗАКУПКИ'
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=None, dtype=str)

    # Столбцы, в которые нужно вставить данные
    columns_to_fill = [32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56]
    columns_to_fill_ = [31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55]

    # Заполняем значения в первой строке данными из второй строки
    for col in columns_to_fill:
        df.iloc[0, col] = df.iloc[1, col]

    # Применяем функцию clean_string ко всем именам столбцов
    for col in range(df.shape[1]):
        df.iloc[0, col] = clean_string(df.iloc[0, col])

    for col in columns_to_fill_:
        df.iloc[0, col] = clean_string(df.iloc[0, col]) + ' ' + str('дата оплаты')

    df.iloc[0, 32] = 'Январь (факт)' + ' ' + clean_string(df.iloc[0, 32])
    df.iloc[0, 34] = 'Февраль (факт)' + ' ' + clean_string(df.iloc[0, 34])
    df.iloc[0, 36] = 'Февраль (факт)' + ' ' + clean_string(df.iloc[0, 36])
    df.iloc[0, 38] = 'Февраль (факт)' + ' ' + clean_string(df.iloc[0, 38])
    df.iloc[0, 40] = 'Февраль (факт)' + ' ' + clean_string(df.iloc[0, 40])
    df.iloc[0, 42] = 'Февраль (факт)' + ' ' + clean_string(df.iloc[0, 42])
    df.iloc[0, 44] = 'Февраль (факт)' + ' ' + clean_string(df.iloc[0, 44])
    df.iloc[0, 46] = 'Февраль (факт)' + ' ' + clean_string(df.iloc[0, 46])
    df.iloc[0, 48] = 'Февраль (факт)' + ' ' + clean_string(df.iloc[0, 48])
    df.iloc[0, 50] = 'Февраль (факт)' + ' ' + clean_string(df.iloc[0, 50])
    df.iloc[0, 52] = 'Февраль (факт)' + ' ' + clean_string(df.iloc[0, 52])
    df.iloc[0, 54] = 'Февраль (факт)' + ' ' + clean_string(df.iloc[0, 54])
    df.iloc[0, 56] = 'Февраль (факт)' + ' ' + clean_string(df.iloc[0, 56])

    # file_path = 'C:/Users/neverov/Desktop/gos.xlsx'
    # sheet_name = 'ЗАКУПКИ'  # Замените на имя вашего листа
    # df = pd.read_excel(file_path, sheet_name=sheet_name, header=None, dtype=str) # Читаем все как строки
    # print(df.iloc[0].fillna(''))
    # exit()
    # df = pd.read_excel(file_path, sheet_name=sheet_name, header=2,
    #                 dtype={'№ п/п': str, 'Наименование закупки': str,
    #                     'Статус (Выбор из списка констант)': str, 'Способ закупки (Выбор из списка констант)': str, 'Инициатор закупки (ИТ/АХО) (Выбор из списка констант)': str,
    #                     'КЦСР (Выбор из списка констант)': str, 'КОСГУ (Выбор из списка констант)': str, 'ДопФК (Выбор из списка констант)': str,
    #                     'НМЦК': str, 'Экономия': str, 'Контрагент': str,
    #                     'Реестровый номер контракта (ЕИС)': str, 'Номер контракта': str, 'Дата контракта': str,
    #                     'Окончание даты исполнения': str, 'Цена контракта (на 2024 год)': str, 'Исполнение контракта (план) (формула)': str,
    #                     'Январь (план)': str,
    #                     'Февраль (план)': str, 'Март (план)': str, 'Апрель (план)': str,
    #                     'Май (план)': str, 'Июнь (план)': str, 'Июль (план)': str,
    #                     'Август (план)': str, 'Сентябрь (план)': str, 'Октябрь (план)': str,
    #                     'Ноябрь (план)': str, 'Декабрь (план)': str, 'Январь (план)': str,
    #                     'Исполнение контракта (факт) (формула)': str, 'дата оплаты': str, 'сумма оплаты': str,
    #                     'Февраль (план)': str, 'Март (план)': str, 'Апрель (план)': str,
    #                     'Февраль (план)': str, 'Март (план)': str, 'Апрель (план)': str,
    #                     'Февраль (план)': str, 'Март (план)': str, 'Апрель (план)': str,
    #                     'Февраль (план)': str, 'Март (план)': str, 'Апрель (план)': str,
    #                     'Февраль (план)': str, 'Март (план)': str, 'Апрель (план)': str,
    #                     'Февраль (план)': str, 'Март (план)': str, 'Апрель (план)': str,
    #                     'Февраль (план)': str, 'Март (план)': str, 'Апрель (план)': str,
    #                     'Февраль (план)': str, 'Март (план)': str, 'Апрель (план)': str,
    #                     'Февраль (план)': str, 'Март (план)': str, 'Апрель (план)': str,
    #                     'Февраль (план)': str, 'Март (план)': str, 'Апрель (план)': str,
    #                     'Февраль (план)': str, 'Март (план)': str, 'Апрель (план)': str,
    #                     'Февраль (план)': str, 'Март (план)': str, 'Апрель (план)': str,
    #                     'Февраль (план)': str, 'Март (план)': str, 'Апрель (план)': str,
    #                     'Февраль (план)': str, 'Март (план)': str, 'Апрель (план)': str,
    #                     'Февраль (план)': str, 'Март (план)': str, 'Апрель (план)': str,
    #                     'Февраль (план)': str, 'Март (план)': str, 'Апрель (план)': str,
    #                     'Февраль (план)': str, 'Март (план)': str, 'Апрель (план)': str,
    #                     'Февраль (план)': str, 'Март (план)': str, 'Апрель (план)': str,
    #                     'Февраль (план)': str, 'Март (план)': str, 'Апрель (план)': str,
    #                     'Февраль (план)': str, 'Март (план)': str, 'Апрель (план)': str})

    def extract_number(value, default="0.0"):
        """Извлекает первое число из строки, если оно есть."""
        import re
        match = re.search(r"[-+]?\d*[,\.]\d+|\d+", str(value))
        if match:
            number = match.group(0).replace(',', '.') # Заменяем запятую на точку
            if number.endswith(".0"):
                number = number[:-2] # Удаляем ".0" в конце
            return number
            # return match.group(0).replace(',', '.')  # Заменяем запятую на точку для поддержки формата float
        return default

    def extract_date_and_number(value):
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
        if pd.isna(value):
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

        return str(value) # Возвращаем None, если не удалось распарсить дату

    def safe_conversion(value):
        """Для преобразования данных"""
        if pd.isna(value):
            return ''
        return str(value)  # Преобразуем в строку, если значение не NaN

    def convert_to_float(x):
        # Удаляем неразрывные пробелы и другие пробелы
        if isinstance(x, str):
            x = x.replace('\xa0', '').strip()  # Удаляем неразрывные пробелы и обрезаем пробелы
        try:
            return float(x) if pd.notnull(x) and x != '' else None
        except ValueError:
            return 'None'  # Возвращаем None, если не удалось конвертировать

    def safe_float_conversion(value):
        print('----')
        print(value)
        print('----')
        # exit()
        # Если value является Series, извлекаем первое значение
        if isinstance(value, pd.Series):
            # Применяем конвертацию ко всем элементам Series
            return value.apply(lambda x: convert_to_float(x))

        # print('POPAL1', value)
        """Для преобразолвания в float"""
        if pd.isna(value):
            return "0.0"
        try:
            number_str = extract_number(float(value))
            return f"{number_str}"
        except ValueError:
            return "0.0"

    def safe_int_conversion(value):
        """Для преобразования в int"""
        if pd.isna(value):
            return "0"
        try:
            number_str = extract_number(value)
            return f"{number_str}"
        except ValueError:
            return "0"

    # # Выводим первую строку для проверки
    # print(df.iloc[0].fillna(''))
    # exit()

    df.columns = df.iloc[0]  # Используем первую строку как заголовки столбцов
    df = df.drop(0)  # Удаляем первую строку, так как она теперь используется как заголовок
    df = df.drop(1)  # Удаляем первую строку, так как она теперь используется как заголовок

    print(df[1])
    exit()


    df[f'{df.iloc[0, 29]}'] = df[f'{df.iloc[0, 29]}'].apply(safe_float_conversion)
    exit()

    df[f'{df.iloc[0, 0]}'] = df[f'{df.iloc[0, 0]}'].iloc[2:].apply(safe_conversion)
    df[f'{df.iloc[0, 1]}'] = df[f'{df.iloc[0, 1]}'].iloc[2:].apply(safe_conversion)
    df[f'{df.iloc[0, 2]}'] = df[f'{df.iloc[0, 2]}'].iloc[2:].apply(safe_conversion)
    df[f'{df.iloc[0, 3]}'] = df[f'{df.iloc[0, 3]}'].iloc[2:].apply(safe_conversion)
    df[f'{df.iloc[0, 4]}'] = df[f'{df.iloc[0, 4]}'].iloc[2:].apply(safe_conversion)
    df[f'{df.iloc[0, 5]}'] = df[f'{df.iloc[0, 5]}'].iloc[2:].apply(safe_int_conversion)
    df[f'{df.iloc[0, 6]}'] = df[f'{df.iloc[0, 6]}'].iloc[2:].apply(safe_int_conversion)
    df[f'{df.iloc[0, 7]}'] = df[f'{df.iloc[0, 7]}'].iloc[2:].apply(safe_int_conversion)
    df[f'{df.iloc[0, 8]}'] = df[f'{df.iloc[0, 8]}'].iloc[2:].apply(safe_float_conversion)
    df[f'{df.iloc[0, 9]}'] = df[f'{df.iloc[0, 9]}'].iloc[2:].apply(safe_int_conversion)
    df[f'{df.iloc[0, 10]}'] = df[f'{df.iloc[0, 10]}'].iloc[2:].apply(safe_conversion)
    df[f'{df.iloc[0, 11]}'] = df[f'{df.iloc[0, 11]}'].iloc[2:].apply(safe_int_conversion)
    df[f'{df.iloc[0, 12]}'] = df[f'{df.iloc[0, 12]}'].iloc[2:].apply(safe_conversion)
    df[f'{df.iloc[0, 13]}'] = df[f'{df.iloc[0, 13]}'].iloc[2:].apply(safe_date_conversion)
    df[f'{df.iloc[0, 14]}'] = df[f'{df.iloc[0, 14]}'].iloc[2:].apply(safe_date_conversion)
    df[f'{df.iloc[0, 15]}'] = df[f'{df.iloc[0, 15]}'].iloc[2:].apply(safe_float_conversion)
    df[f'{df.iloc[0, 16]}'] = df[f'{df.iloc[0, 16]}'].iloc[2:].apply(safe_float_conversion)
    df[f'{df.iloc[0, 17]}'] = df[f'{df.iloc[0, 17]}'].iloc[2:].apply(safe_float_conversion)
    df[f'{df.iloc[0, 18]}'] = df[f'{df.iloc[0, 18]}'].iloc[2:].apply(safe_float_conversion)
    df[f'{df.iloc[0, 19]}'] = df[f'{df.iloc[0, 19]}'].iloc[2:].apply(safe_float_conversion)
    df[f'{df.iloc[0, 20]}'] = df[f'{df.iloc[0, 20]}'].iloc[2:].apply(safe_float_conversion)
    df[f'{df.iloc[0, 21]}'] = df[f'{df.iloc[0, 21]}'].iloc[2:].apply(safe_float_conversion)
    df[f'{df.iloc[0, 22]}'] = df[f'{df.iloc[0, 22]}'].iloc[2:].apply(safe_float_conversion)
    df[f'{df.iloc[0, 23]}'] = df[f'{df.iloc[0, 23]}'].iloc[2:].apply(safe_float_conversion)
    df[f'{df.iloc[0, 24]}'] = df[f'{df.iloc[0, 24]}'].iloc[2:].apply(safe_float_conversion)
    df[f'{df.iloc[0, 25]}'] = df[f'{df.iloc[0, 25]}'].iloc[2:].apply(safe_float_conversion)
    df[f'{df.iloc[0, 26]}'] = df[f'{df.iloc[0, 26]}'].iloc[2:].apply(safe_float_conversion)
    df[f'{df.iloc[0, 27]}'] = df[f'{df.iloc[0, 27]}'].iloc[2:].apply(safe_float_conversion)
    df[f'{df.iloc[0, 28]}'] = df[f'{df.iloc[0, 28]}'].iloc[2:].apply(safe_float_conversion)
    df[f'{df.iloc[0, 29]}'] = df[f'{df.iloc[0, 29]}'].iloc[2:].apply(safe_float_conversion)
    exit()
    df[f'{df.iloc[0, 30]}'] = df[f'{df.iloc[0, 30]}'].iloc[2:].apply(safe_float_conversion)
    df[f'{df.iloc[0, 31]}'] = df[f'{df.iloc[0, 31]}'].iloc[2:].apply(safe_date_conversion)
    df[f'{df.iloc[0, 32]}'] = df[f'{df.iloc[0, 32]}'].iloc[2:].apply(safe_float_conversion)
    df[f'{df.iloc[0, 33]}'] = df[f'{df.iloc[0, 33]}'].iloc[2:].apply(safe_date_conversion)
    df[f'{df.iloc[0, 34]}'] = df[f'{df.iloc[0, 34]}'].iloc[2:].apply(safe_float_conversion)
    df[f'{df.iloc[0, 35]}'] = df[f'{df.iloc[0, 35]}'].iloc[2:].apply(safe_date_conversion)
    df[f'{df.iloc[0, 36]}'] = df[f'{df.iloc[0, 36]}'].iloc[2:].apply(safe_float_conversion)
    df[f'{df.iloc[0, 37]}'] = df[f'{df.iloc[0, 37]}'].iloc[2:].apply(safe_date_conversion)
    df[f'{df.iloc[0, 38]}'] = df[f'{df.iloc[0, 38]}'].iloc[2:].apply(safe_float_conversion)
    df[f'{df.iloc[0, 39]}'] = df[f'{df.iloc[0, 39]}'].iloc[2:].apply(safe_date_conversion)
    df[f'{df.iloc[0, 40]}'] = df[f'{df.iloc[0, 40]}'].iloc[2:].apply(safe_float_conversion)
    df[f'{df.iloc[0, 41]}'] = df[f'{df.iloc[0, 41]}'].iloc[2:].apply(safe_date_conversion)
    df[f'{df.iloc[0, 42]}'] = df[f'{df.iloc[0, 42]}'].iloc[2:].apply(safe_float_conversion)
    df[f'{df.iloc[0, 43]}'] = df[f'{df.iloc[0, 43]}'].iloc[2:].apply(safe_date_conversion)
    df[f'{df.iloc[0, 44]}'] = df[f'{df.iloc[0, 44]}'].iloc[2:].apply(safe_float_conversion)
    df[f'{df.iloc[0, 45]}'] = df[f'{df.iloc[0, 45]}'].iloc[2:].apply(safe_date_conversion)
    df[f'{df.iloc[0, 46]}'] = df[f'{df.iloc[0, 46]}'].iloc[2:].apply(safe_float_conversion)
    df[f'{df.iloc[0, 47]}'] = df[f'{df.iloc[0, 47]}'].iloc[2:].apply(safe_date_conversion)
    df[f'{df.iloc[0, 48]}'] = df[f'{df.iloc[0, 48]}'].iloc[2:].apply(safe_float_conversion)
    df[f'{df.iloc[0, 49]}'] = df[f'{df.iloc[0, 49]}'].iloc[2:].apply(safe_date_conversion)
    df[f'{df.iloc[0, 50]}'] = df[f'{df.iloc[0, 50]}'].iloc[2:].apply(safe_float_conversion)
    df[f'{df.iloc[0, 51]}'] = df[f'{df.iloc[0, 51]}'].iloc[2:].apply(safe_date_conversion)
    df[f'{df.iloc[0, 52]}'] = df[f'{df.iloc[0, 52]}'].iloc[2:].apply(safe_float_conversion)
    df[f'{df.iloc[0, 53]}'] = df[f'{df.iloc[0, 35]}'].iloc[2:].apply(safe_date_conversion)
    df[f'{df.iloc[0, 54]}'] = df[f'{df.iloc[0, 54]}'].iloc[2:].apply(safe_float_conversion)
    df[f'{df.iloc[0, 55]}'] = df[f'{df.iloc[0, 55]}'].iloc[2:].apply(safe_date_conversion)
    df[f'{df.iloc[0, 56]}'] = df[f'{df.iloc[0, 56]}'].iloc[2:].apply(safe_float_conversion)
    df[f'{df.iloc[0, 57]}'] = df[f'{df.iloc[0, 57]}'].iloc[2:].apply(safe_conversion)
    df[f'{df.iloc[0, 58]}'] = df[f'{df.iloc[0, 58]}'].iloc[2:].apply(safe_float_conversion)

    # # Примените функцию для извлечения даты и номера решения об отказе
    # df['Дата решения об отказе в выдаче сертификата'], df['№ решения об отказе в выдаче сертификата'] = zip(*df['Дата и № решения об отказе в выдаче сертификата'].apply(extract_date_and_number))

    # # Заполните NaN значения в DataFrame и обработайте данные
    # df['№ п/п'] = df['№ п/п'].apply(safe_conversion)
    # df['ФИО заявителя'] = df['ФИО заявителя'].apply(safe_conversion)
    # df['СНИЛС'] = df['СНИЛС'].apply(safe_int_conversion)
    # df['Район'] = df['Район'].apply(safe_conversion)
    # df['Адрес нп'] = df['Адрес нп'].apply(safe_conversion)
    # df['Адрес'] = df['Адрес'].apply(safe_conversion)
    # df['Льгота'] = df['Льгота'].apply(safe_conversion)
    # df['Серия и № сертификата'] = df['Серия и № сертификата'].apply(safe_conversion)
    # df['Дата выдачи сертификата'] = df['Дата выдачи сертификата'].apply(safe_date_conversion)
    # df['Размер выплаты'] = df['Размер выплаты'].apply(safe_float_conversion)
    # df['Сертификат'] = df['Сертификат'].apply(safe_int_conversion)
    # df['Дата и № решения о выдаче сертификата'] = df['Дата и № решения о выдаче сертификата'].apply(safe_conversion)
    # df['Дата и № решения об аннулировании сертификата'] = df['Дата и № решения об аннулировании сертификата'].apply(safe_conversion)

    # df['Отказ в выдаче сертификата'] = df['Отказ в выдаче сертификата'].apply(safe_int_conversion)
    # df['Основная причина отказа (пункт)'] = df['Основная причина отказа (пункт)'].apply(safe_conversion)
    # df['ТРЕК'] = df['ТРЕК'].apply(safe_conversion)
    # df['Дата отправки почтой'] = df['Дата отправки почтой'].apply(safe_conversion)

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

    # Подготовьте данные для вставки
    data_to_insert = []
    for _, row in df.iterrows():
        if pd.notna(row.get('Наименование закупки')) and row.get('Наименование закупки').strip():
            # # Проверяем значение 'Сертификат' для заполнения колонки 'Цвет'
            # certificate_value = safe_int_conversion(row.get('Сертификат'))
            # refusal_value = safe_int_conversion(row.get('Отказ в выдаче сертификата'))
            # color_value = "#dff0d8" if certificate_value == "0" and refusal_value == '0' else ""

            color_value = ''

            data_row = (
                # safe_conversion(row.get('№ п/п')),
                # safe_conversion(row.get('ФИО заявителя')),
                # safe_int_conversion(row.get('СНИЛС')),
                # safe_conversion(row.get('Район')),
                # safe_conversion(row.get('Адрес нп')),
                # safe_conversion(row.get('Адрес')),
                # safe_conversion(row.get('Льгота')),
                # safe_conversion(row.get('Серия и № сертификата')),
                # safe_date_conversion(row.get('Дата выдачи сертификата')),
                # safe_float_conversion(row.get('Размер выплаты')),
                # safe_int_conversion(row.get('Сертификат')),
                # safe_conversion(row.get('Дата и № решения о выдаче сертификата')),
                # safe_conversion(row.get('Дата и № решения об аннулировании сертификата')),

                # safe_conversion(row.get('Дата решения об отказе в выдаче сертификата')),
                # safe_conversion(row.get('№ решения об отказе в выдаче сертификата')),

                # safe_int_conversion(row.get('Отказ в выдаче сертификата')),
                # safe_conversion(row.get('Основная причина отказа (пункт)')),
                # safe_conversion(row.get('ТРЕК')),
                # safe_conversion(row.get('Дата отправки почтой')),
                # "",  # Пустая строка для поля 'comment'
                # color_value,

                safe_conversion(row.get(f'{df.iloc[0, 0]}')),
                safe_conversion(row.get(f'{df.iloc[0, 1]}')),
                safe_conversion(row.get(f'{df.iloc[0, 2]}')),
                safe_conversion(row.get(f'{df.iloc[0, 3]}')),
                safe_conversion(row.get(f'{df.iloc[0, 4]}')),
                safe_int_conversion(row.get(f'{df.iloc[0, 5]}')),
                safe_int_conversion(row.get(f'{df.iloc[0, 6]}')),
                safe_int_conversion(row.get(f'{df.iloc[0, 7]}')),
                safe_float_conversion(row.get(f'{df.iloc[0, 8]}')),
                safe_int_conversion(row.get(f'{df.iloc[0, 9]}')),
                safe_conversion(row.get(f'{df.iloc[0, 10]}')),
                safe_int_conversion(row.get(f'{df.iloc[0, 11]}')),
                safe_conversion(row.get(f'{df.iloc[0, 12]}')),
                safe_date_conversion(row.get(f'{df.iloc[0, 13]}')),
                safe_date_conversion(row.get(f'{df.iloc[0, 14]}')),
                safe_float_conversion(row.get(f'{df.iloc[0, 15]}')),
                safe_float_conversion(row.get(f'{df.iloc[0, 16]}')),
                safe_float_conversion(row.get(f'{df.iloc[0, 17]}')),
                safe_float_conversion(row.get(f'{df.iloc[0, 18]}')),
                safe_float_conversion(row.get(f'{df.iloc[0, 19]}')),
                safe_float_conversion(row.get(f'{df.iloc[0, 20]}')),
                safe_float_conversion(row.get(f'{df.iloc[0, 21]}')),
                safe_float_conversion(row.get(f'{df.iloc[0, 22]}')),
                safe_float_conversion(row.get(f'{df.iloc[0, 23]}')),
                safe_float_conversion(row.get(f'{df.iloc[0, 24]}')),
                safe_float_conversion(row.get(f'{df.iloc[0, 25]}')),
                safe_float_conversion(row.get(f'{df.iloc[0, 26]}')),
                safe_float_conversion(row.get(f'{df.iloc[0, 27]}')),
                safe_float_conversion(row.get(f'{df.iloc[0, 28]}')),
                safe_float_conversion(row.get(f'{df.iloc[0, 29]}')),
                safe_float_conversion(row.get(f'{df.iloc[0, 30]}')),
                safe_date_conversion(row.get(f'{df.iloc[0, 31]}')),
                safe_float_conversion(row.get(f'{df.iloc[0, 32]}')),
                safe_date_conversion(row.get(f'{df.iloc[0, 33]}')),
                safe_float_conversion(row.get(f'{df.iloc[0, 34]}')),
                safe_date_conversion(row.get(f'{df.iloc[0, 35]}')),
                safe_float_conversion(row.get(f'{df.iloc[0, 36]}')),
                safe_date_conversion(row.get(f'{df.iloc[0, 37]}')),
                safe_float_conversion(row.get(f'{df.iloc[0, 38]}')),
                safe_date_conversion(row.get(f'{df.iloc[0, 39]}')),
                safe_float_conversion(row.get(f'{df.iloc[0, 40]}')),
                safe_date_conversion(row.get(f'{df.iloc[0, 41]}')),
                safe_float_conversion(row.get(f'{df.iloc[0, 42]}')),
                safe_date_conversion(row.get(f'{df.iloc[0, 43]}')),
                safe_float_conversion(row.get(f'{df.iloc[0, 44]}')),
                safe_date_conversion(row.get(f'{df.iloc[0, 45]}')),
                safe_float_conversion(row.get(f'{df.iloc[0, 46]}')),
                safe_date_conversion(row.get(f'{df.iloc[0, 47]}')),
                safe_float_conversion(row.get(f'{df.iloc[0, 48]}')),
                safe_date_conversion(row.get(f'{df.iloc[0, 49]}')),
                safe_float_conversion(row.get(f'{df.iloc[0, 50]}')),
                safe_date_conversion(row.get(f'{df.iloc[0, 51]}')),
                safe_float_conversion(row.get(f'{df.iloc[0, 52]}')),
                safe_date_conversion(row.get(f'{df.iloc[0, 53]}')),
                safe_float_conversion(row.get(f'{df.iloc[0, 54]}')),
                safe_date_conversion(row.get(f'{df.iloc[0, 55]}')),
                safe_float_conversion(row.get(f'{df.iloc[0, 56]}')),
                safe_conversion(row.get(f'{df.iloc[0, 57]}')),
                safe_float_conversion(row.get(f'{df.iloc[0, 58]}'))

                )

            data_to_insert.append(data_row)

    if data_to_insert:
        # Вставьте данные в базу данных
        cursor.executemany(insert_query, data_to_insert)
        conn.commit()
        print('Данные загружены')
    else:
        print('Данные НЕ загружены')

except Exception as e:
    # Вывод подробной информации об ошибке
    print(f"Поймано исключение: {type(e).__name__}")
    print(f"Сообщение об ошибке: {str(e)}")
    import traceback
    print("Трассировка стека (stack trace):")
    traceback.print_exc()

finally:
    # Закройте соединение
    cursor.close()
    conn.close()