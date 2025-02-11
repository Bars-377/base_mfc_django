import pandas as pd

try:
    # Загрузите данные из Excel
    file_path = 'C:/Users/neverov/Desktop/gos.xlsx'
    sheet_name = 'ЗАКУПКИ'
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=None, dtype=str)

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

    list = []

    for col in range(df.shape[1]):
        list.append(df.iloc[0, col])

    def convert_to_float(x):
        # Удаляем неразрывные пробелы и другие пробелы
        if isinstance(x, str):
            x = x.replace('\xa0', '').strip()  # Удаляем неразрывные пробелы и обрезаем пробелы
        try:
            return float(x) if pd.notnull(x) and x != '' else None
        except ValueError:
            return 'None'  # Возвращаем None, если не удалось конвертировать

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

        return str(value) # Возвращаем None, если не удалось распарсить дату

    def safe_conversion(value):
        """Для преобразования данных"""
        # Если value является Series, извлекаем первое значение
        if isinstance(value, pd.Series):
            # Применяем конвертацию ко всем элементам Series
            return value.apply(lambda x: convert_to_float(x))
        elif pd.isna(value):
            return ''
        return str(value)  # Преобразуем в строку, если значение не NaN

    def safe_float_conversion(value):
        # print('----')
        # print(value)
        # print('----')
        # Если value является Series, извлекаем первое значение
        if isinstance(value, pd.Series):
            # Применяем конвертацию ко всем элементам Series
            return value.apply(lambda x: convert_to_float(x))
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

    df.columns = df.iloc[0]  # Используем первую строку как заголовки столбцов
    df = df.drop(0)  # Удаляем первую строку, так как она теперь используется как заголовок
    df = df.drop(1)  # Удаляем вторую строку, так как она теперь используется как заголовок

    # df[f'{list[31]}'] = df[f'{list[31]}'].apply(safe_date_conversion)
    # exit()

    df[f'{list[0]}'] = df[f'{list[0]}'].apply(safe_conversion)
    df[f'{list[1]}'] = df[f'{list[1]}'].apply(safe_conversion)
    df[f'{list[2]}'] = df[f'{list[2]}'].apply(safe_conversion)
    df[f'{list[3]}'] = df[f'{list[3]}'].apply(safe_conversion)
    df[f'{list[4]}'] = df[f'{list[4]}'].apply(safe_conversion)
    df[f'{list[5]}'] = df[f'{list[5]}'].apply(safe_int_conversion)
    df[f'{list[6]}'] = df[f'{list[6]}'].apply(safe_int_conversion)
    df[f'{list[7]}'] = df[f'{list[7]}'].apply(safe_int_conversion)
    df[f'{list[8]}'] = df[f'{list[8]}'].apply(safe_float_conversion)
    df[f'{list[9]}'] = df[f'{list[9]}'].apply(safe_int_conversion)
    df[f'{list[10]}'] = df[f'{list[10]}'].apply(safe_conversion)
    df[f'{list[11]}'] = df[f'{list[11]}'].apply(safe_int_conversion)
    df[f'{list[12]}'] = df[f'{list[12]}'].apply(safe_conversion)
    df[f'{list[13]}'] = df[f'{list[13]}'].apply(safe_date_conversion)
    df[f'{list[14]}'] = df[f'{list[14]}'].apply(safe_date_conversion)
    df[f'{list[15]}'] = df[f'{list[15]}'].apply(safe_float_conversion)
    df[f'{list[16]}'] = df[f'{list[16]}'].apply(safe_float_conversion)
    df[f'{list[17]}'] = df[f'{list[17]}'].apply(safe_float_conversion)
    df[f'{list[18]}'] = df[f'{list[18]}'].apply(safe_float_conversion)
    df[f'{list[19]}'] = df[f'{list[19]}'].apply(safe_float_conversion)
    df[f'{list[20]}'] = df[f'{list[20]}'].apply(safe_float_conversion)
    df[f'{list[21]}'] = df[f'{list[21]}'].apply(safe_float_conversion)
    df[f'{list[22]}'] = df[f'{list[22]}'].apply(safe_float_conversion)
    df[f'{list[23]}'] = df[f'{list[23]}'].apply(safe_float_conversion)
    df[f'{list[24]}'] = df[f'{list[24]}'].apply(safe_float_conversion)
    df[f'{list[25]}'] = df[f'{list[25]}'].apply(safe_float_conversion)
    df[f'{list[26]}'] = df[f'{list[26]}'].apply(safe_float_conversion)
    df[f'{list[27]}'] = df[f'{list[27]}'].apply(safe_float_conversion)
    df[f'{list[28]}'] = df[f'{list[28]}'].apply(safe_float_conversion)
    df[f'{list[29]}'] = df[f'{list[29]}'].apply(safe_float_conversion)
    df[f'{list[30]}'] = df[f'{list[30]}'].apply(safe_float_conversion)
    df[f'{list[31]}'] = df[f'{list[31]}'].apply(safe_date_conversion)
    df[f'{list[32]}'] = df[f'{list[32]}'].apply(safe_float_conversion)
    df[f'{list[33]}'] = df[f'{list[33]}'].apply(safe_conversion)
    df[f'{list[34]}'] = df[f'{list[34]}'].apply(safe_float_conversion)
    df[f'{list[35]}'] = df[f'{list[35]}'].apply(safe_conversion)
    df[f'{list[36]}'] = df[f'{list[36]}'].apply(safe_float_conversion)
    df[f'{list[37]}'] = df[f'{list[37]}'].apply(safe_conversion)
    df[f'{list[38]}'] = df[f'{list[38]}'].apply(safe_float_conversion)
    df[f'{list[39]}'] = df[f'{list[39]}'].apply(safe_conversion)
    df[f'{list[40]}'] = df[f'{list[40]}'].apply(safe_float_conversion)
    df[f'{list[41]}'] = df[f'{list[41]}'].apply(safe_conversion)
    df[f'{list[42]}'] = df[f'{list[42]}'].apply(safe_float_conversion)
    df[f'{list[43]}'] = df[f'{list[43]}'].apply(safe_conversion)
    df[f'{list[44]}'] = df[f'{list[44]}'].apply(safe_float_conversion)
    df[f'{list[45]}'] = df[f'{list[45]}'].apply(safe_conversion)
    df[f'{list[46]}'] = df[f'{list[46]}'].apply(safe_float_conversion)
    df[f'{list[47]}'] = df[f'{list[47]}'].apply(safe_conversion)
    df[f'{list[48]}'] = df[f'{list[48]}'].apply(safe_float_conversion)
    df[f'{list[49]}'] = df[f'{list[49]}'].apply(safe_conversion)
    df[f'{list[50]}'] = df[f'{list[50]}'].apply(safe_float_conversion)
    df[f'{list[51]}'] = df[f'{list[51]}'].apply(safe_conversion)
    df[f'{list[52]}'] = df[f'{list[52]}'].apply(safe_float_conversion)
    df[f'{list[53]}'] = df[f'{list[53]}'].apply(safe_conversion)
    df[f'{list[54]}'] = df[f'{list[54]}'].apply(safe_float_conversion)
    df[f'{list[55]}'] = df[f'{list[55]}'].apply(safe_conversion)
    df[f'{list[56]}'] = df[f'{list[56]}'].apply(safe_float_conversion)
    df[f'{list[57]}'] = df[f'{list[57]}'].apply(safe_conversion)
    df[f'{list[58]}'] = df[f'{list[58]}'].apply(safe_float_conversion)

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

    # Преобразуем DataFrame в список кортежей
    data_to_insert = [tuple(x) for x in df.to_numpy()]

    # Преобразование всех значений в строки и добавление пустой строки в конец каждого кортежа
    data_to_insert = [
        tuple(str(value) if value is not None else '' for value in row) + ('',)
        for row in data_to_insert
    ]

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