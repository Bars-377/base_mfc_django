from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Services, Services_Two, Services_Three, Services_backup_one, Services_backup_two
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render
import re
from asgiref.sync import sync_to_async
import asyncio
from .admin import group_required
import logging
from .processors import ContractProcessor
from .common import format_number, log_user_action, errors

# def has_more_than_two_decimal_places(number):
#     """Проверка на двузначный остаток числа"""
#     # Преобразуем число в строку
#     number_str = str(number)

#     # Проверяем, есть ли десятичная точка
#     if '.' in number_str:
#         # Получаем часть после десятичной точки
#         decimal_part = number_str.split('.')[1]
#         # Проверяем, больше ли длина части после запятой двух знаков
#         return len(decimal_part) > 2
#     return False

# async def reduce_number(value):
#     """Форматируем число"""
#     return round(value, 2)

async def get_invalid_costs(qs, field_name):
    return await sync_to_async(list, thread_sensitive=True)(qs.values_list(field_name, flat=True))
    # return await sync_to_async(qs.values_list, thread_sensitive=True)(field_name, flat=True)

async def calculate_costs(query, keyword_one=None, selected_column_one=None, keyword_two=None, selected_column_two=None):
    from django.db.models import Q

    total_cost_111, total_cost_222, total_cost_333 = 0, 0, 0

    filtered_query = query

    # Определите функцию для суммирования стоимостей
    def sum_costs(costs):
        return sum(float(cost) for cost in costs if str(cost).replace('.', '', 1).isdigit())

    # Получите недопустимые затраты для каждого типа
    invalid_costs_nmcc = await get_invalid_costs(filtered_query, 'NMCC')
    invalid_costs_contract_price = await get_invalid_costs(filtered_query, 'contract_price')
    invalid_costs_execution_contract_fact = await get_invalid_costs(filtered_query, 'execution_contract_fact')

    # Суммируйте затраты
    total_cost_111 = sum_costs(invalid_costs_nmcc)
    total_cost_222 = sum_costs(invalid_costs_contract_price)
    total_cost_333 = sum_costs(invalid_costs_execution_contract_fact)

    return total_cost_111, total_cost_222, total_cost_333

from channels.db import database_sync_to_async

async def calculate_total_budget(query_user, string):
    @database_sync_to_async
    def get_values():
        return list(query_user.values_list(string, flat=True))

    count = await get_values()

    def convert_to_number(value):
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.00

    total_cost = sum(convert_to_number(value) for value in count)
    return total_cost

from django.conf import settings

import os
project_dir = os.path.dirname(os.path.abspath(__file__))
folder_path = os.path.join(project_dir, '..', '..')
folder_path = os.path.abspath(folder_path)
# Открываем файл и загружаем данные
with open(f'{folder_path}//general_settings.json', 'r', encoding='utf-8-sig') as file:
    json_object = json.load(file)

def link_generation(request, mode, page, page_user='', page_user_two='', service=None, row_id=None):
    # print('---------------------')
    # print('request', request)
    # print('mode', mode)
    # print('page', page)
    # print('page_user', page_user)
    # print('page_user_two', page_user_two)
    # print('service', service)
    # print('row_id', row_id)
    # print('---------------------')
    # exit()
    # Списки имён параметров для получения из GET-запроса
    params_with_int_default_1 = [page, page_user, page_user_two]
    params_with_int_default_1 = [p for p in params_with_int_default_1 if p != '']

    user = request.user

    params_optional = [
        'keyword_one',
        'keyword_two',
        'keyword_three',
        'keyword_four',
        'selected_column_one',
        'selected_column_two',
        'selected_column_three',
        'selected_column_four',
        'contract_date',
        'end_date'
    ]

    # Создаем словарь для хранения результатов
    params = {}

    # Получаем остальные параметры без преобразования
    for param in params_optional:
        if param in ('contract_date', 'end_date'):
            params[f'selected_{param}'] = request.GET.get(param, "No")
        else:
            params[param] = request.GET.get(param, None)

    # Получаем параметры с преобразованием в int и значением по умолчанию 1
    for param in params_with_int_default_1:
        try:
            params[param] = int(request.GET.get(param, 1))
        except ValueError:
            params[param] = 1  # На случай, если параметр не преобразуется в int

    if mode:
        SSR = [request, user]

        for key in params:
            SSR.append(params[key])

        return SSR
    else:
        if service and row_id:
            # Подготовка контекста для шаблона
            context = {
                'service': service,
                'row_id': row_id,
                'connection_websocket': settings.DATABASES['default']['HOST'],
                'statuses': json.dumps(json_object['statuses'])
            }
        else:
            # Подготовка контекста для шаблона
            context = {
                'user': user,
                'connection_websocket': settings.DATABASES['default']['HOST'],
                'statuses': json.dumps(json_object['statuses'])
            }

        for key in params:
            context[key] = params[key]

        return context

async def skeleton(request, user,
                    keyword_one, keyword_two, keyword_three,
                    keyword_four, selected_column_one, selected_column_two,
                    selected_column_three, selected_column_four,
                    contract_date, end_date,
                    # KOSGU_user,
                    # keyword_one_user, keyword_two_user,
                    # selected_column_one_user, selected_column_two_user,
                    # KOSGU_user_two,
                    # keyword_one_user_two, keyword_two_user_two,
                    # selected_column_one_user_two, selected_column_two_user_two,
                    page,
                    page_user,
                    page_user_two):
    async def remove_spaces_if_numeric(text):
        stripped_text = text.replace(" ", "")  # Удаляем все пробелы
        if all(char.isdigit() or char in "+-*/.()" for char in stripped_text):
            return stripped_text
        return text

    async def format_input(variable):
        return None if variable == 'None' else variable

    async def format_input_remove(variable):
        return None if variable == 'None' or variable == None else await remove_spaces_if_numeric(str(variable).strip())

    contract_date = await format_input(contract_date)
    end_date = await format_input(end_date)
    keyword_one = await format_input_remove(keyword_one)
    keyword_two = await format_input_remove(keyword_two)

    selected_column_one = await format_input(selected_column_one)
    selected_column_two = await format_input(selected_column_two)

    keyword_three = await format_input_remove(keyword_three)
    keyword_four = await format_input_remove(keyword_four)

    selected_column_three = await format_input(selected_column_three)
    selected_column_four = await format_input(selected_column_four)

    # KOSGU_user = await format_input(KOSGU_user)
    # keyword_one_user = await format_input_remove(keyword_one_user)
    # keyword_two_user = await format_input_remove(keyword_two_user)

    # selected_column_one_user = await format_input(selected_column_one_user)
    # selected_column_two_user = await format_input(selected_column_two_user)

    # KOSGU_user_two = await format_input(KOSGU_user_two)
    # keyword_one_user_two = await format_input_remove(keyword_one_user_two)
    # keyword_two_user_two = await format_input_remove(keyword_two_user_two)

    # selected_column_one_user_two = await format_input(selected_column_one_user_two)
    # selected_column_two_user_two = await format_input(selected_column_two_user_two)

    per_page = 20

    # Получаем все уникальные значения year и date_number_no_one
    all_years = await sync_to_async(lambda: list(Services.objects.values('contract_date').distinct()), thread_sensitive=True)()
    all_end_date = await sync_to_async(lambda: list(Services.objects.values('end_date').distinct()), thread_sensitive=True)()
    # all_KOSGU_user = await sync_to_async(lambda: list(Services_Two.objects.values('KOSGU').distinct()), thread_sensitive=True)()
    # all_KOSGU_user_two = await sync_to_async(lambda: list(Services_Three.objects.values('KOSGU').distinct()), thread_sensitive=True)()

    # Регулярные выражения для форматов дат
    pattern_dd_mm_yyyy = r'\b\d{2}\.\d{2}\.\d{4}\b'
    pattern_yyyy_mm_dd = r'\b\d{4}-\d{2}-\d{2}\b'

    @sync_to_async
    def findall_sync(pattern, text):
        return re.findall(pattern, text)

    async def process_service_data(all_data, field_name):
        service_data = set()
        empty_found = False

        for item in all_data:
            field_value = item.get(field_name, None)
            if not field_value:
                empty_found = True
                continue

            matches_dd_mm_yyyy = await findall_sync(pattern_dd_mm_yyyy, field_value)
            matches_yyyy_mm_dd = await findall_sync(pattern_yyyy_mm_dd, field_value)

            service_data.update([date_str[-4:] for date_str in matches_dd_mm_yyyy])
            service_data.update([date_str[:4] for date_str in matches_yyyy_mm_dd])

        service_data = sorted({str(int(year)) for year in service_data if year.isdigit()})
        if empty_found:
            service_data.insert(0, 'None')
        return service_data

    async def process_service_KOSGU(all_data, field_name):
        service_data = set()
        empty_found = False

        for item in all_data:
            field_value = item.get(field_name, None)
            if not field_value:
                empty_found = True
                continue

            service_data.add(field_value)

        service_data = sorted({str(int(year)) for year in service_data if year.isdigit()})
        if empty_found:
            service_data.insert(0, 'None')
        return service_data

    service_years = await process_service_data(all_years, 'contract_date')
    service_end_date = await process_service_data(all_end_date, 'end_date')
    # service_KOSGU_user = await process_service_KOSGU(all_KOSGU_user, 'KOSGU')
    # service_KOSGU_user_two = await process_service_KOSGU(all_KOSGU_user_two, 'KOSGU')

    # Построение запроса
    query = await sync_to_async(Services.objects.all, thread_sensitive=True)()
    query_user = await sync_to_async(Services_Two.objects.all, thread_sensitive=True)()
    query_user_two = await sync_to_async(Services_Three.objects.all, thread_sensitive=True)()

    if contract_date == 'No':
        contract_date = None
    if end_date == 'No':
        end_date = None

    async def apply_filters(query, filters):
        for filter_func in filters:
            query = await sync_to_async(filter_func)(query)
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

    query = await apply_filters(query, filters)

    # if KOSGU_user == 'No':
    #     KOSGU_user = None

    # if KOSGU_user_two == 'No':
    #     KOSGU_user_two = None

    # if KOSGU_user == 'None':
    #     query_user = query_user.exclude(Q(KOSGU__regex=pattern_dd_mm_yyyy) | Q(KOSGU__regex=pattern_yyyy_mm_dd))
    # elif KOSGU_user:
    #     query_user = query_user.filter(KOSGU__icontains=KOSGU_user)

    # if KOSGU_user_two == 'None':
    #     query_user_two = query_user_two.exclude(Q(KOSGU__regex=pattern_dd_mm_yyyy) | Q(KOSGU__regex=pattern_yyyy_mm_dd))
    # elif KOSGU_user_two:
    #     query_user_two = query_user_two.filter(KOSGU__icontains=KOSGU_user_two)

    async def apply_keyword_filter(query, keyword, column, model):
        if keyword:
            if column and hasattr(model, column):
                query = query.filter(**{column + '__icontains': keyword})
            else:
                filters = Q()
                for field in model._meta.get_fields():
                    filters |= Q(**{field.name + '__icontains': keyword})
                query = query.filter(filters)
        return query

    query = await apply_keyword_filter(query, keyword_one, selected_column_one, Services)
    query = await apply_keyword_filter(query, keyword_two, selected_column_two, Services)

    query = await apply_keyword_filter(query, keyword_three, selected_column_three, Services)
    query = await apply_keyword_filter(query, keyword_four, selected_column_four, Services)

    # query_user = await apply_keyword_filter(query_user, keyword_one_user, selected_column_one_user, Services_Two)
    # query_user = await apply_keyword_filter(query_user, keyword_two_user, selected_column_two_user, Services_Two)
    # query_user_two = await apply_keyword_filter(query_user_two, keyword_one_user_two, selected_column_one_user_two, Services_Three)
    # query_user_two = await apply_keyword_filter(query_user_two, keyword_two_user_two, selected_column_two_user_two, Services_Three)

    # Сортировка
    from django.db.models import IntegerField
    from django.db.models.functions import Cast

    # Преобразование id_id в целое число и contract_date в дату перед сортировкой
    query = query.annotate(
        id_id_int=Cast('id_id', IntegerField())
    ).order_by('id_id_int')

    # Преобразование id_id в целое число и KOSGU в целое число перед сортировкой
    query_user = query_user.annotate(
        kosgu_int=Cast('KOSGU', IntegerField())  # Преобразование KOSGU в целое число
    ).order_by('kosgu_int')  # Сортировка по id_id_int и kosgu_int

    # Преобразование id_id в целое число и KOSGU в целое число перед сортировкой
    query_user_two = query_user_two.annotate(
        kosgu_int=Cast('KOSGU', IntegerField())  # Преобразование KOSGU в целое число
    ).order_by('kosgu_int')  # Сортировка по id_id_int и kosgu_int

    # Логика подсчета стоимости

    # total_cost_1 = await calculate_total_budget(query_user, 'budget_limit')
    # total_cost_2 = await calculate_total_budget(query_user, 'off_budget_limit')
    # total_cost_3 = await calculate_total_budget(query_user, 'budget_planned')
    # total_cost_4 = await calculate_total_budget(query_user, 'off_budget_planned')
    # total_cost_5 = await calculate_total_budget(query_user, 'budget_bargaining')
    # total_cost_6 = await calculate_total_budget(query_user, 'off_budget_bargaining')
    # total_cost_7 = await calculate_total_budget(query_user, 'budget_concluded')
    # total_cost_8 = await calculate_total_budget(query_user, 'off_budget_concluded')
    # total_cost_9 = await calculate_total_budget(query_user, 'budget_completed')
    # total_cost_10 = await calculate_total_budget(query_user, 'off_budget_completed')
    # total_cost_11 = await calculate_total_budget(query_user, 'budget_execution')
    # total_cost_12 = await calculate_total_budget(query_user, 'off_budget_execution')
    # total_cost_13 = await calculate_total_budget(query_user, 'budget_remainder')
    # total_cost_14 = await calculate_total_budget(query_user, 'off_budget_remainder')
    # total_cost_15 = await calculate_total_budget(query_user, 'budget_plans')
    # total_cost_16 = await calculate_total_budget(query_user, 'off_budget_plans')

    categories = [
        'budget_limit', 'off_budget_limit',
        'budget_planned', 'off_budget_planned',
        'budget_bargaining', 'off_budget_bargaining',
        'budget_concluded', 'off_budget_concluded',
        'budget_completed', 'off_budget_completed',
        'budget_execution', 'off_budget_execution',
        'budget_remainder', 'off_budget_remainder',
        'budget_plans', 'off_budget_plans',
    ]

    total_costs = {}

    for i, category in enumerate(categories, start=1):
        total_costs[f'total_cost_{i}'] = await calculate_total_budget(query_user, category)

    try:
        total_cost_17 = total_costs['total_cost_1'] + total_costs['total_cost_2']
        total_cost_18 = ((total_costs['total_cost_11'] + total_costs['total_cost_12']) / total_cost_17) * 100
        total_cost_18 = round(total_cost_18, 2)  # Округляем до двух знаков после запятой
    except:
        total_cost_17 = 0.00
        total_cost_18 = 0.00

    # Получаем все записи из таблицы Services_Three
    Services_Three_ = await sync_to_async(list, thread_sensitive=True)(Services_Three.objects.all())

    total_cost_1_11 = 0.00
    total_cost_1_22 = 0.00
    total_cost_1_1 = 0.00
    total_cost_1_2 = 0.00
    total_cost_1_3 = 0.00
    total_cost_1_4 = 0.00
    total_cost_1_5 = 0.00
    total_cost_1_6 = 0.00

    for service in Services_Three_:
        total_cost_1_11 += await format_number(service.budget_planned_old)
        total_cost_1_22 += await format_number(service.off_budget_planned_old)
        total_cost_1_1 += await format_number(service.budget_planned)
        total_cost_1_2 += await format_number(service.off_budget_planned)
        total_cost_1_3 += await format_number(service.budget_concluded)
        total_cost_1_4 += await format_number(service.off_budget_concluded)
        total_cost_1_5 += await format_number(service.budget_remainder)
        total_cost_1_6 += await format_number(service.off_budget_remainder)

    total_cost_1_7 = total_cost_17 - (total_cost_1_3 + total_cost_1_4)

    total_cost_111, total_cost_222, total_cost_333 = await calculate_costs(query)

    # Пагинация
    paginator = Paginator(query, per_page)
    services = await sync_to_async(paginator.get_page)(page)

    # Пагинация
    paginator_user = Paginator(query_user, 30)
    services_user = await sync_to_async(paginator_user.get_page)(page_user)

    # Пагинация
    paginator_user_two = Paginator(query_user_two, 30)
    services_user_two = await sync_to_async(paginator_user_two.get_page)(page_user_two)

    # Получаем общее количество страниц
    total_pages = paginator.num_pages

    # Получаем общее количество страниц
    total_pages_user = paginator_user.num_pages

    # Получаем общее количество страниц
    total_pages_user_two = paginator_user_two.num_pages

    # Определяем максимальное количество кнопок для навигации
    max_page_buttons = 5
    start_page = max(1, page - max_page_buttons // 2)
    end_page = min(total_pages, page + max_page_buttons // 2)

    # Определяем максимальное количество кнопок для навигации
    max_page_buttons_user = 5
    start_page_user = max(1, page_user - max_page_buttons_user // 2)
    end_page_user = min(total_pages_user, page_user + max_page_buttons_user // 2)

    # Определяем максимальное количество кнопок для навигации
    max_page_buttons_user_two = 5
    start_page_user_two = max(1, page_user_two - max_page_buttons_user_two // 2)
    end_page_user_two = min(total_pages_user_two, page_user + max_page_buttons_user_two // 2)

    if end_page - start_page < max_page_buttons - 1:
        if start_page > 1:
            end_page = min(total_pages, end_page + (max_page_buttons - (end_page - start_page)))
        else:
            start_page = max(1, end_page - (max_page_buttons - (end_page - start_page)))

    if end_page_user - start_page_user < max_page_buttons_user - 1:
        if start_page_user > 1:
            end_page_user = min(total_pages_user, end_page_user + (max_page_buttons_user - (end_page_user - start_page_user)))
        else:
            start_page_user = max(1, end_page_user - (max_page_buttons_user - (end_page_user - start_page_user)))

    if end_page_user_two - start_page_user_two < max_page_buttons_user_two - 1:
        if start_page_user_two > 1:
            end_page_user_two = min(total_pages_user_two, end_page_user_two + (max_page_buttons_user_two - (end_page_user_two - start_page_user_two)))
        else:
            start_page_user_two = max(1, end_page_user_two - (max_page_buttons_user_two - (end_page_user_two - start_page_user_two)))

    pages = range(start_page, end_page + 1)  # Создаем диапазон страниц

    pages_user = range(start_page_user, end_page_user + 1)  # Создаем диапазон страниц

    pages_user_two = range(start_page_user_two, end_page_user_two + 1)  # Создаем диапазон страниц

    # Подготовка контекста для шаблона
    context = {
        'data': services,
        'data_user': services_user,
        'data_user_two': services_user_two,
        'user': user,
        'pages': pages,
        'pages_user': pages_user,
        'pages_user_two': pages_user_two,
        'total_cost_1': round(await format_number(total_costs['total_cost_1']), 2),
        'total_cost_2': round(await format_number(total_costs['total_cost_2']), 2),
        'total_cost_3': round(await format_number(total_costs['total_cost_3']), 2),
        'total_cost_4': round(await format_number(total_costs['total_cost_4']), 2),
        'total_cost_5': round(await format_number(total_costs['total_cost_5']), 2),
        'total_cost_6': round(await format_number(total_costs['total_cost_6']), 2),
        'total_cost_7': round(await format_number(total_costs['total_cost_7']), 2),
        'total_cost_8': round(await format_number(total_costs['total_cost_8']), 2),
        'total_cost_9': round(await format_number(total_costs['total_cost_9']), 2),
        'total_cost_10': round(await format_number(total_costs['total_cost_10']), 2),
        'total_cost_11': round(await format_number(total_costs['total_cost_11']), 2),
        'total_cost_12': round(await format_number(total_costs['total_cost_12']), 2),
        'total_cost_13': round(await format_number(total_costs['total_cost_13']), 2),
        'total_cost_14': round(await format_number(total_costs['total_cost_14']), 2),
        'total_cost_15': round(await format_number(total_costs['total_cost_15']), 2),
        'total_cost_16': round(await format_number(total_costs['total_cost_16']), 2),
        'total_cost_17': round(await format_number(total_cost_17), 2),
        'total_cost_18': round(await format_number(total_cost_18), 2),
        'total_cost_1_11': round(await format_number(total_cost_1_11), 2),
        'total_cost_1_22': round(await format_number(total_cost_1_22), 2),
        'total_cost_1_1': round(await format_number(total_cost_1_1), 2),
        'total_cost_1_2': round(await format_number(total_cost_1_2), 2),
        'total_cost_1_3': round(await format_number(total_cost_1_3), 2),
        'total_cost_1_4': round(await format_number(total_cost_1_4), 2),
        'total_cost_1_5': round(await format_number(total_cost_1_5), 2),
        'total_cost_1_6': round(await format_number(total_cost_1_6), 2),
        'total_cost_1_7': round(await format_number(total_cost_1_7), 2),
        'total_cost_111': round(await format_number(total_cost_111), 2),
        'total_cost_222': round(await format_number(total_cost_222), 2),
        'total_cost_333': round(await format_number(total_cost_333), 2),
        'selected_contract_date': contract_date,
        # 'selected_KOSGU_user': KOSGU_user,
        # 'selected_KOSGU_user_two': KOSGU_user_two,
        'selected_end_date': end_date,
        'selected_column_one': selected_column_one,
        'selected_column_three': selected_column_three,
        # 'selected_column_one_user': selected_column_one_user,
        # 'selected_column_one_user_two': selected_column_one_user_two,
        'selected_column_two': selected_column_two,
        'selected_column_four': selected_column_four,
        # 'selected_column_two_user': selected_column_two_user,
        # 'selected_column_two_user_two': selected_column_two_user_two,
        'keyword_one': keyword_one,
        'keyword_three': keyword_three,
        # 'keyword_one_user': keyword_one_user,
        # 'keyword_one_user_two': keyword_one_user_two,
        'keyword_two': keyword_two,
        'keyword_four': keyword_four,
        # 'keyword_two_user': keyword_two_user,
        # 'keyword_two_user_two': keyword_two_user_two,
        'page': page,
        'page_user': page_user,
        'page_user_two': page_user_two,
        'total_pages': total_pages,
        'total_pages_user': total_pages_user,
        'total_pages_user_two': total_pages_user_two,
        'start_page': start_page,
        'start_page_user': start_page_user,
        'start_page_user_two': start_page_user_two,
        'end_page': end_page,
        'end_page_user': end_page_user,
        'end_page_user_two': end_page_user_two,
        'service_years': service_years,
        # 'service_KOSGU_user': service_KOSGU_user,
        # 'service_KOSGU_user_two': service_KOSGU_user_two,
        'service_end_date': service_end_date,
        'connection_websocket': settings.DATABASES['default']['HOST'],
        'statuses': json.dumps(json_object['statuses'])
    }

    return await sync_to_async(render)(request, 'data_table.html', context)
    # return await render(request, 'data_table.html', context)

@login_required
async def data_table_view(request):
    user = request.user

    total_pages_full = request.GET.get('total_pages_full', None)
    total_pages_full_user = request.GET.get('total_pages_full_user', None)
    total_pages_full_user_two = request.GET.get('total_pages_full_user_two', None)

    # contract_date = request.GET.get('contract_date', None)
    # end_date = request.GET.get('end_date', None)
    # keyword_one = request.GET.get('keyword_one', None)
    # keyword_two = request.GET.get('keyword_two', None)
    # keyword_three = request.GET.get('keyword_three', None)
    # keyword_four = request.GET.get('keyword_four', None)
    # selected_column_one = request.GET.get('selected_column_one', None)
    # selected_column_two = request.GET.get('selected_column_two', None)
    # selected_column_three = request.GET.get('selected_column_three', None)
    # selected_column_four = request.GET.get('selected_column_four', None)
    # page = int(request.GET.get('page', 1))
    # page_user = int(request.GET.get('page_user', 1))
    # page_user_two = int(request.GET.get('page_user_two', 1))

    SSR = link_generation(request, True, 'page', 'page_user', 'page_user_two')

    # # Списки имён параметров для получения из GET-запроса
    # params_with_int_default_1 = ['page', 'page_user', 'page_user_two']
    # params_optional = [
    #     'keyword_one',
    #     'keyword_two',
    #     'keyword_three',
    #     'keyword_four',
    #     'selected_column_one',
    #     'selected_column_two',
    #     'selected_column_three',
    #     'selected_column_four',
    #     'contract_date',
    #     'end_date',
    #     # 'total_pages_full',
    #     # 'total_pages_full_user',
    #     # 'total_pages_full_user_two',
    # ]

    # # Создаем словарь для хранения результатов
    # params = {}

    # # Получаем остальные параметры без преобразования
    # for param in params_optional:
    #     params[param] = request.GET.get(param, None)

    # # Получаем параметры с преобразованием в int и значением по умолчанию 1
    # for param in params_with_int_default_1:
    #     try:
    #         params[param] = int(request.GET.get(param, 1))
    #     except ValueError:
    #         params[param] = 1  # На случай, если параметр не преобразуется в int

    # SSR = [request, user]

    # for key in params:
    #     SSR.append(params[key])

    per_page = 20

    if total_pages_full:
        # query = await sync_to_async(lambda: Services.objects.all())()
        # query = await sync_to_async(list, thread_sensitive=True)(Services.objects.all())
        query = await sync_to_async(Services.objects.all, thread_sensitive=True)()

        # total_services_full = await sync_to_async(lambda: query.count())()
        # total_services_full = query.count()  # Также без sync_to_async
        total_services_full = await sync_to_async(query.count, thread_sensitive=True)()  # Используем async обертку для count
        page = (total_services_full + per_page - 1) // per_page
        SSR[-3] = page

    if total_pages_full_user:
        # query_user = await sync_to_async(lambda: Services_Two.objects.all())()
        # query_user = await sync_to_async(list, thread_sensitive=True)(Services_Two.objects.all())
        query_user = await sync_to_async(Services_Two.objects.all, thread_sensitive=True)()

        # total_services_full_user = await sync_to_async(lambda: query_user.count())()
        # total_services_full_user = query_user.count()  # Также без sync_to_async
        total_services_full_user = await sync_to_async(query_user.count, thread_sensitive=True)()
        page_user = (total_services_full_user + per_page - 1) // per_page
        SSR[-2] = page_user

    if total_pages_full_user_two:
        # query_user_two = await sync_to_async(lambda: Services_Three.objects.all())()
        # query_user_two = await sync_to_async(list, thread_sensitive=True)(Services_Three.objects.all())
        query_user_two = await sync_to_async(Services_Three.objects.all, thread_sensitive=True)()

        # total_services_full_user_two = await sync_to_async(lambda: query_user_two.count())()
        # total_services_full_user_two = query_user_two.count()  # Также без sync_to_async
        total_services_full_user_two = await sync_to_async(query_user_two.count, thread_sensitive=True)()
        page_user_two = (total_services_full_user_two + per_page - 1) // per_page
        SSR[-1] = page_user_two

    # KOSGU_user = request.GET.get('KOSGU_user', None)
    # keyword_one_user = request.GET.get('keyword_one_user', None)
    # keyword_two_user = request.GET.get('keyword_two_user', None)
    # selected_column_one_user = request.GET.get('selected_column_one_user', None)
    # selected_column_two_user = request.GET.get('selected_column_two_user', None)

    # KOSGU_user_two = request.GET.get('KOSGU_user_two', None)
    # keyword_one_user_two = request.GET.get('keyword_one_user_two', None)
    # keyword_two_user_two = request.GET.get('keyword_two_user_two', None)
    # selected_column_one_user_two = request.GET.get('selected_column_one_user_two', None)
    # selected_column_two_user_two = request.GET.get('selected_column_two_user_two', None)

    return await skeleton(*SSR)

    # return await skeleton(request, user,
    #                 contract_date, end_date,
    #                 keyword_one, keyword_two,
    #                 selected_column_one, selected_column_two,
    #                 # KOSGU_user,
    #                 # keyword_one_user, keyword_two_user,
    #                 # selected_column_one_user, selected_column_two_user,
    #                 # KOSGU_user_two,
    #                 # keyword_one_user_two, keyword_two_user_two,
    #                 # selected_column_one_user_two, selected_column_two_user_two,

    #                 keyword_four, selected_column_three,
    #                 selected_column_four, keyword_three,
    #                 page,
    #                 page_user,
    #                 page_user_two)

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User

# async def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = await sync_to_async(authenticate)(request, username=username, password=password)
#         if user is not None:
#             await sync_to_async(login)(request, user)
#             return redirect('data_table_view')  # Переход на страницу после успешного входа
#         else:
#             await sync_to_async(messages.error)(request, "Неверное имя пользователя или пароль")
#     return await sync_to_async(render)(request, 'login.html')  # Ваш шаблон для входа

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('data_table_view')  # Переход на страницу после успешного входа
        else:
            messages.error(request, "Неверное имя пользователя или пароль")
    return render(request, 'login.html')  # Ваш шаблон для входа

# Асинхронная обертка для создания пользователя
@sync_to_async
def create_user(username, email, password):
    return User.objects.create_user(username=username, email=email, password=password)

# async def register_view(request):
#     await log_user_action(request.user, 'Регистрируется')
#     if request.method == 'POST':
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']
#         confirm_password = request.POST['confirm_password']

#         if password == confirm_password:
#             await create_user(username=username, email=email, password=password)
#             await sync_to_async(messages.success)(request, "Регистрация прошла успешно. Вы можете войти.")
#             return redirect('login')
#         else:
#             await sync_to_async(messages.error)(request, "Пароли не совпадают")
#     return await sync_to_async(render)(request, 'register.html')  # Ваш шаблон для регистрации

async def register_view(request):
    await log_user_action(request.user, 'Регистрируется')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            await create_user(username=username, email=email, password=password)
            messages.success(request, "Регистрация прошла успешно. Вы можете войти.")
            return redirect('login')
        else:
            messages.error(request, "Пароли не совпадают")
    return render(request, 'register.html')  # Ваш шаблон для регистрации

@group_required('Администратор', 'Полный')
@csrf_exempt  # Необходимо, если вы не используете CSRF-токены
async def update_color(request, row_id):
    await log_user_action(request.user, f'Обновил цвет записи в "Закупки" с ID {row_id}')
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            color = data.get('color')

            # Найдите запись по ID и обновите цвет
            service = await sync_to_async(Services.objects.get, thread_sensitive=True)(id=row_id)
            service.color = color
            await sync_to_async(service.save)()

            return JsonResponse({'success': True, 'id': service.id, 'color': service.color}, status=200)
        except Services.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Service not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON.'}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)

@csrf_exempt  # Необходимо, если вы не используете CSRF-токены
async def update_color_user(request, row_id):
    await log_user_action(request.user, f'Обновил цвет записи в "План-график" с ID {row_id}')
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            color = data.get('color')

            # Найдите запись по ID и обновите цвет
            service = await sync_to_async(Services_Two.objects.get, thread_sensitive=True)(id=row_id)
            service.color = color
            await sync_to_async(service.save)()

            return JsonResponse({'success': True, 'id': service.id, 'color': service.color})
        except Services_Two.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Service not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON.'}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)

@csrf_exempt  # Необходимо, если вы не используете CSRF-токены
async def update_color_user_two(request, row_id):
    await log_user_action(request.user, f'Обновил цвет записи в "План-график" с ID {row_id}')
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            color = data.get('color')

            # Найдите запись по ID и обновите цвет
            service = await sync_to_async(Services_Three.objects.get, thread_sensitive=True)(id=row_id)
            service.color = color
            await sync_to_async(service.save)()

            return JsonResponse({'success': True, 'id': service.id, 'color': service.color})
        except Services_Two.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Service not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON.'}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)

@group_required('Администратор', 'Полный')
@csrf_exempt  # Необходимо, если вы не используете CSRF-токены
async def add(request):
    await log_user_action(request.user, f'Перешёл на страницу добавления записи в "Закупки"')

    # keyword_one = request.GET.get('keyword_one', None)
    # keyword_two = request.GET.get('keyword_two', None)
    # keyword_three = request.GET.get('keyword_three', None)
    # keyword_four = request.GET.get('keyword_four', None)
    # selected_column_one = request.GET.get('selected_column_one', None)
    # selected_column_two = request.GET.get('selected_column_two', None)
    # selected_column_three = request.GET.get('selected_column_three', None)
    # selected_column_four = request.GET.get('selected_column_four', None)
    # selected_contract_date = request.GET.get('contract_date', "No")
    # selected_end_date = request.GET.get('end_date', "No")
    # page = int(request.GET.get('page', 1))
    # total_pages = int(request.GET.get('total_pages', 1))

    # user = request.user

    context = link_generation(request, False, 'page', 'total_pages')

    # # Списки имён параметров для получения из GET-запроса
    # params_with_int_default_1 = ['page', 'total_pages']
    # params_optional = [
    #     'keyword_one',
    #     'keyword_two',
    #     'keyword_three',
    #     'keyword_four',
    #     'selected_column_one',
    #     'selected_column_two',
    #     'selected_column_three',
    #     'selected_column_four',
    #     'contract_date',
    #     'end_date'
    # ]

    # # Создаем словарь для хранения результатов
    # params = {}

    # # Получаем остальные параметры без преобразования
    # for param in params_optional:
    #     if param in ('contract_date', 'end_date'):
    #         params[f'selected_{param}'] = request.GET.get(param, "No")
    #     else:
    #         params[param] = request.GET.get(param, None)

    # # Получаем параметры с преобразованием в int и значением по умолчанию 1
    # for param in params_with_int_default_1:
    #     try:
    #         params[param] = int(request.GET.get(param, 1))
    #     except ValueError:
    #         params[param] = 1  # На случай, если параметр не преобразуется в int

    # # Подготовка контекста для шаблона
    # context = {
    #     'user': user,
    #     'connection_websocket': settings.DATABASES['default']['HOST'],
    #     'statuses': json.dumps(json_object['statuses'])
    # }

    # for key in params:
    #     context[key] = params[key]

    # # Подготовка контекста для шаблона
    # context = {
    #     'user': user,
    #     'page': page,
    #     'keyword_one': keyword_one,
    #     'keyword_two': keyword_two,
    #     'keyword_three': keyword_three,
    #     'keyword_four': keyword_four,
    #     'selected_column_one': selected_column_one,
    #     'selected_column_two': selected_column_two,
    #     'selected_column_three': selected_column_three,
    #     'selected_column_four': selected_column_four,
    #     'selected_contract_date': selected_contract_date,
    #     'selected_end_date': selected_end_date,
    #     'total_pages': total_pages,
    #     'connection_websocket': settings.DATABASES['default']['HOST'],
    #     'statuses': json.dumps(json_object['statuses'])
    # }

    return await sync_to_async(render)(request, 'add.html', context)
    # return await render(request, 'add.html', context)

@group_required('Администратор', 'Полный')
@csrf_exempt  # Необходимо, если вы не используете CSRF-токены
async def add_two(request):
    await log_user_action(request.user, f'Перешёл на страницу добавления записи в "Свод"')

    # keyword_one = request.GET.get('keyword_one', None)
    # keyword_two = request.GET.get('keyword_two', None)
    # keyword_three = request.GET.get('keyword_three', None)
    # keyword_four = request.GET.get('keyword_four', None)
    # selected_column_one = request.GET.get('selected_column_one', None)
    # selected_column_two = request.GET.get('selected_column_two', None)
    # selected_column_three = request.GET.get('selected_column_three', None)
    # selected_column_four = request.GET.get('selected_column_four', None)
    # selected_contract_date = request.GET.get('contract_date', "No")
    # selected_end_date = request.GET.get('end_date', "No")
    # page = int(request.GET.get('page', 1))
    # total_pages = int(request.GET.get('total_pages', 1))

    # user = request.user

    # # Подготовка контекста для шаблона
    # context = {
    #     'user': user,
    #     'page': page,
    #     'keyword_one': keyword_one,
    #     'keyword_two': keyword_two,
    #     'keyword_three': keyword_three,
    #     'keyword_four': keyword_four,
    #     'selected_column_one': selected_column_one,
    #     'selected_column_two': selected_column_two,
    #     'selected_column_three': selected_column_three,
    #     'selected_column_four': selected_column_four,
    #     'selected_contract_date': selected_contract_date,
    #     'selected_end_date': selected_end_date,
    #     'total_pages': total_pages,
    #     'connection_websocket': settings.DATABASES['default']['HOST'],
    #     'statuses': json.dumps(json_object['statuses'])
    # }

    # user = request.user

    context = link_generation(request, False, 'page', 'total_pages')

    # # Списки имён параметров для получения из GET-запроса
    # params_with_int_default_1 = ['page', 'total_pages']
    # params_optional = [
    #     'keyword_one',
    #     'keyword_two',
    #     'keyword_three',
    #     'keyword_four',
    #     'selected_column_one',
    #     'selected_column_two',
    #     'selected_column_three',
    #     'selected_column_four',
    #     'contract_date',
    #     'end_date'
    # ]

    # # Создаем словарь для хранения результатов
    # params = {}

    # # Получаем остальные параметры без преобразования
    # for param in params_optional:
    #     if param in ('contract_date', 'end_date'):
    #         params[f'selected_{param}'] = request.GET.get(param, "No")
    #     else:
    #         params[param] = request.GET.get(param, None)

    # # Получаем параметры с преобразованием в int и значением по умолчанию 1
    # for param in params_with_int_default_1:
    #     try:
    #         params[param] = int(request.GET.get(param, 1))
    #     except ValueError:
    #         params[param] = 1  # На случай, если параметр не преобразуется в int

    # # Подготовка контекста для шаблона
    # context = {
    #     'user': user,
    #     'connection_websocket': settings.DATABASES['default']['HOST'],
    #     'statuses': json.dumps(json_object['statuses'])
    # }

    # for key in params:
    #     context[key] = params[key]

    return await sync_to_async(render)(request, 'add_two.html', context)
    # return render(request, 'add_two.html', context)

@group_required('Администратор', 'Полный', 'Редактирование-Закупки')
@csrf_exempt  # Необходимо, если вы не используете CSRF-токены
async def edit(request, row_id):
    await log_user_action(request.user, f'Перешёл на страницу редактирования записи в "Закупки" с ID {row_id}')

    # page = int(request.GET.get('page', 1))
    # keyword_one = request.GET.get('keyword_one', None)
    # keyword_two = request.GET.get('keyword_two', None)
    # keyword_three = request.GET.get('keyword_three', None)
    # keyword_four = request.GET.get('keyword_four', None)
    # selected_column_one = request.GET.get('selected_column_one', None)
    # selected_column_two = request.GET.get('selected_column_two', None)
    # selected_column_three = request.GET.get('selected_column_three', None)
    # selected_column_four = request.GET.get('selected_column_four', None)
    # selected_contract_date = request.GET.get('contract_date', "No")
    # selected_end_date = request.GET.get('end_date', "No")

    # Получаем объект service по id
    service = await sync_to_async(Services.objects.get, thread_sensitive=True)(id=row_id)

    context = link_generation(request, False, 'page', service=service, row_id=row_id)

    context['status'] = ''
    context['way'] = ''
    context['KTSSR'] = ''
    context['KOSGU'] = ''
    context['DopFC'] = ''

    # # Списки имён параметров для получения из GET-запроса
    # params_with_int_default_1 = ['page']
    # params_optional = [
    #     'keyword_one',
    #     'keyword_two',
    #     'keyword_three',
    #     'keyword_four',
    #     'selected_column_one',
    #     'selected_column_two',
    #     'selected_column_three',
    #     'selected_column_four',
    #     'contract_date',
    #     'end_date'
    # ]

    # # Создаем словарь для хранения результатов
    # params = {}

    # # Получаем остальные параметры без преобразования
    # for param in params_optional:
    #     if param in ('contract_date', 'end_date'):
    #         params[f'selected_{param}'] = request.GET.get(param, "No")
    #     else:
    #         params[param] = request.GET.get(param, None)

    # # Получаем параметры с преобразованием в int и значением по умолчанию 1
    # for param in params_with_int_default_1:
    #     try:
    #         params[param] = int(request.GET.get(param, 1))
    #     except ValueError:
    #         params[param] = 1  # На случай, если параметр не преобразуется в int

    # # Подготовка контекста для шаблона
    # context = {
    #     'service': service,
    #     'row_id': row_id,
    #     'connection_websocket': settings.DATABASES['default']['HOST'],
    #     'statuses': json.dumps(json_object['statuses'])
    # }

    # for key in params:
    #     context[key] = params[key]

    # # Подготовка контекста для шаблона
    # context = {
    #     'service': service,
    #     'status': '',
    #     'way': '',
    #     'KTSSR': '',
    #     'KOSGU': '',
    #     'DopFC': '',
    #     'row_id': row_id,
    #     'page': page,
    #     'keyword_one': keyword_one,
    #     'keyword_two': keyword_two,
    #     'keyword_three': keyword_three,
    #     'keyword_four': keyword_four,
    #     'selected_column_one': selected_column_one,
    #     'selected_column_two': selected_column_two,
    #     'selected_column_three': selected_column_three,
    #     'selected_column_four': selected_column_four,
    #     'selected_contract_date': selected_contract_date,
    #     'selected_end_date': selected_end_date,
    #     'connection_websocket': settings.DATABASES['default']['HOST'],
    #     'statuses': json.dumps(json_object['statuses'])
    # }

    return await sync_to_async(render)(request, 'edit.html', context)
    # return render(request, 'edit.html', context)

@group_required('Администратор', 'Полный', 'Редактирование-Свод')
@csrf_exempt  # Необходимо, если вы не используете CSRF-токены
async def edit_user(request, row_id):
    await log_user_action(request.user, f'Перешёл на страницу редактирования записи в "Свод" с ID {row_id}')
    # page_user = int(request.GET.get('page_user', 1))
    # # keyword_one_user = request.GET.get('keyword_one_user', None)
    # # keyword_two_user = request.GET.get('keyword_two_user', None)
    # # selected_column_one_user = request.GET.get('selected_column_one_user', None)
    # # selected_column_two_user = request.GET.get('selected_column_two_user', None)

    # Получаем объект service_user по id
    service_user = await sync_to_async(Services_Two.objects.get, thread_sensitive=True)(id=row_id)

    context = link_generation(request, False, 'page_user', service=service_user, row_id=row_id)

    # # Списки имён параметров для получения из GET-запроса
    # params_with_int_default_1 = ['page_user']
    # params_optional = [
    #     'keyword_one',
    #     'keyword_two',
    #     'keyword_three',
    #     'keyword_four',
    #     'selected_column_one',
    #     'selected_column_two',
    #     'selected_column_three',
    #     'selected_column_four',
    #     'contract_date',
    #     'end_date'
    # ]

    # # Создаем словарь для хранения результатов
    # params = {}

    # # Получаем остальные параметры без преобразования
    # for param in params_optional:
    #     if param in ('contract_date', 'end_date'):
    #         params[f'selected_{param}'] = request.GET.get(param, "No")
    #     else:
    #         params[param] = request.GET.get(param, None)

    # # Получаем параметры с преобразованием в int и значением по умолчанию 1
    # for param in params_with_int_default_1:
    #     try:
    #         params[param] = int(request.GET.get(param, 1))
    #     except ValueError:
    #         params[param] = 1  # На случай, если параметр не преобразуется в int

    # # Подготовка контекста для шаблона
    # context = {
    #     'service': service_user,
    #     'row_id': row_id,
    #     'connection_websocket': settings.DATABASES['default']['HOST'],
    #     'statuses': json.dumps(json_object['statuses'])
    # }

    # for key in params:
    #     context[key] = params[key]

    # # Подготовка контекста для шаблона
    # context = {
    #     'service_user': service_user,
    #     'row_id_user': row_id,
    #     'page_user': page_user,
    #     # 'keyword_one_user': keyword_one_user,
    #     # 'keyword_two_user': keyword_two_user,
    #     # 'selected_column_one_user': selected_column_one_user,
    #     # 'selected_column_two_user': selected_column_two_user,
    #     'connection_websocket': settings.DATABASES['default']['HOST'],
    #     'statuses': json.dumps(json_object['statuses'])
    # }

    return await sync_to_async(render)(request, 'edit_user.html', context)
    # return render(request, 'edit_user.html', context)

@group_required('Администратор', 'Полный')
@csrf_exempt  # Необходимо, если вы не используете CSRF-токены
async def edit_user_two(request, row_id):
    await log_user_action(request.user, f'Перешёл на страницу редактирования записи в "План-график" с ID {row_id}')

    # page_user = int(request.GET.get('page_user', 1))
    # # keyword_one_user = request.GET.get('keyword_one_user', None)
    # # keyword_two_user = request.GET.get('keyword_two_user', None)
    # # selected_column_one_user = request.GET.get('selected_column_one_user', None)
    # # selected_column_two_user = request.GET.get('selected_column_two_user', None)

    # Получаем объект service_user_two по id
    service_user_two = await sync_to_async(Services_Three.objects.get, thread_sensitive=True)(id=row_id)

    context = link_generation(request, False, 'page_user_two', service=service_user_two, row_id=row_id)

    # # Списки имён параметров для получения из GET-запроса
    # params_with_int_default_1 = ['page_user_two']
    # params_optional = [
    #     'keyword_one',
    #     'keyword_two',
    #     'keyword_three',
    #     'keyword_four',
    #     'selected_column_one',
    #     'selected_column_two',
    #     'selected_column_three',
    #     'selected_column_four',
    #     'contract_date',
    #     'end_date'
    # ]

    # # Создаем словарь для хранения результатов
    # params = {}

    # # Получаем остальные параметры без преобразования
    # for param in params_optional:
    #     if param in ('contract_date', 'end_date'):
    #         params[f'selected_{param}'] = request.GET.get(param, "No")
    #     else:
    #         params[param] = request.GET.get(param, None)

    # # Получаем параметры с преобразованием в int и значением по умолчанию 1
    # for param in params_with_int_default_1:
    #     try:
    #         params[param] = int(request.GET.get(param, 1))
    #     except ValueError:
    #         params[param] = 1  # На случай, если параметр не преобразуется в int

    # # Подготовка контекста для шаблона
    # context = {
    #     'service': service_user_two,
    #     'row_id': row_id,
    #     'connection_websocket': settings.DATABASES['default']['HOST'],
    #     'statuses': json.dumps(json_object['statuses'])
    # }

    # for key in params:
    #     context[key] = params[key]

    # # Подготовка контекста для шаблона
    # context = {
    #     'service_user_two': service_user_two,
    #     'row_id_user_two': row_id,
    #     'page_user': page_user,
    #     # 'keyword_one_user': keyword_one_user,
    #     # 'keyword_two_user': keyword_two_user,
    #     # 'selected_column_one_user': selected_column_one_user,
    #     # 'selected_column_two_user': selected_column_two_user,
    #     'connection_websocket': settings.DATABASES['default']['HOST'],
    #     'statuses': json.dumps(json_object['statuses'])
    # }

    return await sync_to_async(render)(request, 'edit_user_two.html', context)
    # return render(request, 'edit_user_two.html', context)

@csrf_exempt  # Необходимо, если вы не используете CSRF-токены
async def update_record(request, row_id):
    if request.method == 'POST':
        try:
            # Возвращаем данные формы обратно в шаблон
            context_data = {
                # 'id_id': request.POST['id_id'],
                # 'name': request.POST['name'],
                # 'status': request.POST['status'],
                # 'way': request.POST['way'],
                # 'initiator': request.POST['initiator'],
                # 'KTSSR': request.POST['KTSSR'],
                # 'KOSGU': request.POST['KOSGU'],
                # 'DopFC': request.POST['DopFC'],
                # 'NMCC': request.POST['NMCC'],
                # 'counterparty': request.POST['counterparty'],
                # 'registration_number': request.POST['registration_number'],
                # 'contract_number': request.POST['contract_number'],
                # 'contract_date': request.POST['contract_date'],
                # 'end_date': request.POST['end_date'],
                # 'contract_price': request.POST['contract_price'],
                # 'january_one': request.POST['january_one'],
                # 'february': request.POST['february'],
                # 'march': request.POST['march'],
                # 'april': request.POST['april'],
                # 'may': request.POST['may'],
                # 'june': request.POST['june'],
                # 'july': request.POST['july'],
                # 'august': request.POST['august'],
                # 'september': request.POST['september'],
                # 'october': request.POST['october'],
                # 'november': request.POST['november'],
                # 'december': request.POST['december'],
                # 'january_two': request.POST['january_two'],
                # 'date_january_one': request.POST['date_january_one'],
                # 'sum_january_one': request.POST['sum_january_one'],
                # 'date_february': request.POST['date_february'],
                # 'sum_february': request.POST['sum_february'],
                # 'date_march': request.POST['date_march'],
                # 'sum_march':  request.POST['sum_march'],
                # 'date_april': request.POST['date_april'],
                # 'sum_april': request.POST['sum_april'],
                # 'date_may': request.POST['date_may'],
                # 'sum_may': request.POST['sum_may'],
                # 'date_june': request.POST['date_june'],
                # 'sum_june': request.POST['sum_june'],
                # 'date_july': request.POST['date_july'],
                # 'sum_july': request.POST['sum_july'],
                # 'date_august': request.POST['date_august'],
                # 'sum_august': request.POST['sum_august'],
                # 'date_september': request.POST['date_september'],
                # 'sum_september': request.POST['sum_september'],
                # 'date_october': request.POST['date_october'],
                # 'sum_october': request.POST['sum_october'],
                # 'date_november': request.POST['date_november'],
                # 'sum_november': request.POST['sum_november'],
                # 'date_december': request.POST['date_december'],
                # 'sum_december': request.POST['sum_december'],
                # 'date_january_two': request.POST['date_january_two'],
                # 'sum_january_two': request.POST['sum_january_two'],
                # 'execution': request.POST['execution'],
                # 'contract_balance': request.POST['contract_balance'],
                # 'execution_contract_fact': request.POST['execution_contract_fact'],
                # 'execution_contract_plan': request.POST['execution_contract_plan'],
                # 'saving': request.POST['saving'],
                # 'color': request.POST['color'],

                'service': await sync_to_async(Services.objects.get, thread_sensitive=True)(id=row_id),
                'row_id': row_id,
                'page': int(request.GET.get('page', '1')) if request.GET.get('page', '1').strip() else 1,
                'page_user': 1,
                'page_user_two': 1,
                'connection_websocket': settings.DATABASES['default']['HOST'],
                'statuses': json.dumps(json_object['statuses']),

                # 'keyword_one': request.GET.get('keyword_one', None),
                # 'keyword_two': request.GET.get('keyword_two', None),
                # 'selected_column_one': request.GET.get('selected_column_one', None),
                # 'selected_column_two': request.GET.get('selected_column_two', None),
                # 'KOSGU_user': request.GET.get('KOSGU_user', None),
                # 'keyword_one_user': request.GET.get('keyword_one_user', None),
                # 'keyword_two_user': request.GET.get('keyword_two_user', None),
                # 'selected_column_one_user': request.GET.get('selected_column_one_user', None),
                # 'selected_column_two_user': request.GET.get('selected_column_two_user', None),
                # 'KOSGU_user_two': request.GET.get('KOSGU_user_two', None),
                # 'keyword_one_user_two': request.GET.get('keyword_one_user_two', None),
                # 'keyword_two_user_two': request.GET.get('keyword_two_user_two', None),
                # 'selected_column_one_user_two': request.GET.get('selected_column_one_user_two', None),
                # 'selected_column_two_user_two': request.GET.get('selected_column_two_user_two', None)
            }

            params = [
                'keyword_one', 'keyword_two', 'keyword_three', 'keyword_four',
                'selected_column_one', 'selected_column_two',
                'contract_date', 'selected_end_date',
                # 'KOSGU_user',
                # 'keyword_one_user', 'keyword_two_user',
                # 'selected_column_one_user', 'selected_column_two_user',
                # 'KOSGU_user_two',
                # 'keyword_one_user_two', 'keyword_two_user_two',
                # 'selected_column_one_user_two', 'selected_column_two_user_two',
            ]

            params_post = [
                'id_id', 'name', 'status', 'way', 'initiator', 'KTSSR',
                'KOSGU', 'DopFC', 'NMCC', 'counterparty',
                'registration_number', 'contract_number', 'contract_date',
                'end_date', 'contract_price', 'january_one',
                'february', 'march', 'april', 'may', 'june', 'july',
                'august', 'september', 'october', 'november', 'december',
                'january_two', 'date_january_one', 'sum_january_one',
                'date_february', 'sum_february', 'date_march', 'sum_march',
                'date_april', 'sum_april', 'date_may', 'sum_may',
                'date_june', 'sum_june', 'date_july', 'sum_july',
                'date_august', 'sum_august', 'date_september', 'sum_september',
                'date_october', 'sum_october', 'date_november', 'sum_november',
                'date_december', 'sum_december', 'date_january_two', 'sum_january_two',
                'execution', 'contract_balance', 'execution_contract_fact', 'execution_contract_plan',
                'saving', 'color', 'remainder_old_year', 'paid_last_year'
            ]

            for param in params:
                context_data[param] = request.GET.get(param, None)

            for param in params_post:
                context_data[param] = request.POST.get(param, None)

            processor = ContractProcessor(context_data, request)
            # print(context_data)
            return await processor.process_update()
        except Services.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Service not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON.'}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)

@csrf_exempt  # Необходимо, если вы не используете CSRF-токены
async def update_record_user(request, row_id):
    if request.method == 'POST':
        try:
            # Возвращаем данные формы обратно в шаблон
            context_data = {
                # 'id_id': request.POST['id_id'],
                # 'name': request.POST['name'],
                # 'KOSGU': request.POST['KOSGU'],
                # 'DopFC': request.POST['DopFC'],
                # 'budget_limit': request.POST['budget_limit'],
                # 'off_budget_limit': request.POST['off_budget_limit'],
                # 'budget_planned': request.POST['budget_planned'],
                # 'off_budget_planned': request.POST['off_budget_planned'],
                # 'budget_bargaining': request.POST['budget_bargaining'],
                # 'off_budget_bargaining': request.POST['off_budget_bargaining'],
                # 'budget_concluded': request.POST['budget_concluded'],
                # 'off_budget_concluded': request.POST['off_budget_concluded'],
                # 'budget_completed': request.POST['budget_completed'],
                # 'off_budget_completed': request.POST['off_budget_completed'],
                # 'budget_completed': request.POST['budget_completed'],
                # 'budget_execution': request.POST['budget_execution'],
                # 'off_budget_execution': request.POST['off_budget_execution'],
                # 'budget_remainder': request.POST['budget_remainder'],
                # 'off_budget_remainder': request.POST['off_budget_remainder'],
                # 'budget_plans': request.POST['budget_plans'],
                # 'off_budget_plans': request.POST['off_budget_plans'],
                # 'color': request.POST['color'],

                'service_user': await sync_to_async(Services_Two.objects.get, thread_sensitive=True)(id=row_id),
                'row_id': row_id,
                'page': int(request.GET.get('page', '1')) if request.GET.get('page', '1').strip() else 1,
                'connection_websocket': settings.DATABASES['default']['HOST'],
                'statuses': json.dumps(json_object['statuses']),
                'page_user': int(request.GET.get('page_user', '1')) if request.GET.get('page', '1').strip() else 1,
                'page_user_two': int(request.GET.get('page_user_two', '1')) if request.GET.get('page', '1').strip() else 1,

                # 'keyword_one': request.GET.get('keyword_one', None),
                # 'keyword_two': request.GET.get('keyword_two', None),
                # 'selected_column_one': request.GET.get('selected_column_one', None),
                # 'selected_column_two': request.GET.get('selected_column_two', None),
                # 'KOSGU_user': request.GET.get('KOSGU_user', None),
                # 'keyword_one_user': request.GET.get('keyword_one_user', None),
                # 'keyword_two_user': request.GET.get('keyword_two_user', None),
                # 'selected_column_one_user': request.GET.get('selected_column_one_user', None),
                # 'selected_column_two_user': request.GET.get('selected_column_two_user', None),
                # 'KOSGU_user_two': request.GET.get('KOSGU_user_two', None),
                # 'keyword_one_user_two': request.GET.get('keyword_one_user_two', None),
                # 'keyword_two_user_two': request.GET.get('keyword_two_user_two', None),
                # 'selected_column_one_user_two': request.GET.get('selected_column_one_user_two', None),
                # 'selected_column_two_user_two': request.GET.get('selected_column_two_user_two', None),
            }

            params = [
                'keyword_one', 'keyword_two', 'keyword_three', 'keyword_four',
                'selected_column_one', 'selected_column_two',
                'contract_date', 'selected_end_date',
                # 'KOSGU_user',
                # 'keyword_one_user','keyword_two_user',
                # 'selected_column_one_user', 'selected_column_two_user',
                # 'KOSGU_user_two',
                # 'keyword_one_user_two', 'keyword_two_user_two',
                # 'selected_column_one_user_two', 'selected_column_two_user_two',
            ]

            params_post = [
                'id_id', 'name', 'KOSGU', 'DopFC', 'budget_limit',
                'off_budget_limit', 'budget_planned', 'off_budget_planned',
                'budget_bargaining', 'off_budget_bargaining', 'budget_concluded',
                'off_budget_concluded', 'budget_completed', 'off_budget_completed',
                'budget_completed', 'budget_execution', 'off_budget_execution',
                'budget_remainder', 'off_budget_remainder', 'budget_plans',
                'off_budget_plans', 'color',
            ]

            for param in params:
                context_data[param] = request.GET.get(param, None)

            for param in params_post:
                context_data[param] = request.POST.get(param, None)

            from django.forms.models import model_to_dict
            service_dict = model_to_dict(context_data['service_user'])
            await log_user_action(request.user, f'Отредактировал запись в "Свод" с ID {service_dict['id_id']},\nБыло: budget_limit: {service_dict['budget_limit']}, off_budget_limit: {service_dict['off_budget_limit']}')

            # context_data['service_user'].id_id = context_data['id_id']
            # context_data['service_user'].name = context_data['name']
            # context_data['service_user'].KOSGU = context_data['KOSGU']
            # context_data['service_user'].DopFC = context_data['DopFC']
            # context_data['service_user'].budget_limit = context_data['budget_limit']
            # context_data['service_user'].off_budget_limit = context_data['off_budget_limit']
            # context_data['service_user'].budget_planned = context_data['budget_planned']
            # context_data['service_user'].off_budget_planned = context_data['off_budget_planned']
            # context_data['service_user'].budget_bargaining = context_data['budget_bargaining']
            # context_data['service_user'].off_budget_bargaining = context_data['off_budget_bargaining']
            # context_data['service_user'].budget_concluded = context_data['budget_concluded']
            # context_data['service_user'].off_budget_concluded = context_data['off_budget_concluded']
            # context_data['service_user'].budget_completed = context_data['budget_completed']
            # context_data['service_user'].off_budget_completed = context_data['off_budget_completed']
            # context_data['service_user'].budget_execution = context_data['budget_execution']
            # context_data['service_user'].off_budget_execution = context_data['off_budget_execution']
            # context_data['service_user'].budget_remainder = context_data['budget_remainder']
            # context_data['service_user'].off_budget_remainder = context_data['off_budget_remainder']
            # context_data['service_user'].budget_plans = context_data['budget_plans']
            # context_data['service_user'].off_budget_plans = context_data['off_budget_plans']
            # context_data['service_user'].color = context_data['color']

            fields_to_copy = [
                'id_id', 'name', 'KOSGU', 'DopFC', 'budget_limit', 'off_budget_limit',
                'budget_planned', 'off_budget_planned', 'budget_bargaining', 'off_budget_bargaining',
                'budget_concluded', 'off_budget_concluded', 'budget_completed', 'off_budget_completed',
                'budget_execution', 'off_budget_execution', 'budget_remainder', 'off_budget_remainder',
                'budget_plans', 'off_budget_plans', 'color'
            ]

            for field in fields_to_copy:
                setattr(context_data['service_user'], field, context_data[field])

            await sync_to_async(context_data['service_user'].save)()

            await log_user_action(request.user, f'Отредактировал запись в "Свод" с ID {context_data['id_id']},\nСтало: budget_limit: {context_data['budget_limit']}, off_budget_limit: {context_data['off_budget_limit']}')

            processor = ContractProcessor(context_data, request)
            return await processor.process_update_user()
        except Services.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Service not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON.'}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)

@csrf_exempt  # Необходимо, если вы не используете CSRF-токены
async def update_record_user_two(request, row_id):
    if request.method == 'POST':
        try:
            # Возвращаем данные формы обратно в шаблон
            context_data = {
                # 'id_id': request.POST['id_id'],
                # 'KOSGU': request.POST['KOSGU'],
                # 'DopFC': request.POST['DopFC'],
                # 'budget_planned_old': request.POST['budget_planned_old'],
                # 'off_budget_planned_old': request.POST['off_budget_planned_old'],
                # 'budget_planned': request.POST['budget_planned'],
                # 'off_budget_planned': request.POST['off_budget_planned'],
                # 'budget_concluded': request.POST['budget_concluded'],
                # 'off_budget_concluded': request.POST['off_budget_concluded'],
                # 'budget_remainder': request.POST['budget_remainder'],
                # 'off_budget_remainder': request.POST['off_budget_remainder'],
                # 'color': request.POST['color'],

                'service_user_two': await sync_to_async(Services_Three.objects.get, thread_sensitive=True)(id=row_id),
                'row_id': row_id,
                'page': int(request.GET.get('page', '1')) if request.GET.get('page', '1').strip() else 1,
                'connection_websocket': settings.DATABASES['default']['HOST'],
                'statuses': json.dumps(json_object['statuses']),
                'page_user': int(request.GET.get('page_user', '1')) if request.GET.get('page', '1').strip() else 1,
                'page_user_two': int(request.GET.get('page_user_two', '1')) if request.GET.get('page', '1').strip() else 1,

                # 'keyword_one': request.GET.get('keyword_one', None),
                # 'keyword_two': request.GET.get('keyword_two', None),
                # 'selected_column_one': request.GET.get('selected_column_one', None),
                # 'selected_column_two': request.GET.get('selected_column_two', None),
                # 'KOSGU_user': request.GET.get('KOSGU_user', None),
                # 'keyword_one_user': request.GET.get('keyword_one_user', None),
                # 'keyword_two_user': request.GET.get('keyword_two_user', None),
                # 'selected_column_one_user': request.GET.get('selected_column_one_user', None),
                # 'selected_column_two_user': request.GET.get('selected_column_two_user', None),
                # 'KOSGU_user_two': request.GET.get('KOSGU_user_two', None),
                # 'keyword_one_user_two': request.GET.get('keyword_one_user_two', None),
                # 'keyword_two_user_two': request.GET.get('keyword_two_user_two', None),
                # 'selected_column_one_user_two': request.GET.get('selected_column_one_user_two', None),
                # 'selected_column_two_user_two': request.GET.get('selected_column_two_user_two', None),
            }

            params = [
                'keyword_one', 'keyword_two', 'keyword_three', 'keyword_four',
                'selected_column_one', 'selected_column_two',
                'contract_date', 'selected_end_date',
                # 'KOSGU_user',
                # 'keyword_one_user', 'keyword_two_user',
                # 'selected_column_one_user', 'selected_column_two_user',
                # 'KOSGU_user_two',
                # 'keyword_one_user_two', 'keyword_two_user_two',
                # 'selected_column_one_user_two', 'selected_column_two_user_two',
            ]

            params_post = [
                'id_id', 'KOSGU', 'DopFC', 'budget_planned_old',
                'off_budget_planned_old', 'budget_planned', 'off_budget_planned',
                'budget_concluded', 'off_budget_concluded', 'budget_remainder',
                'off_budget_remainder', 'color',
            ]

            for param in params:
                context_data[param] = request.GET.get(param, None)

            for param in params_post:
                context_data[param] = request.POST.get(param, None)

            from django.forms.models import model_to_dict
            service_dict = model_to_dict(context_data['service_user_two'])
            await log_user_action(request.user, f'Отредактировал запись в "План-график" с ID {service_dict['id_id']},\nБыло: budget_planned: {service_dict['budget_planned']}, off_budget_planned: {service_dict['off_budget_planned']}')

            # context_data['service_user_two'].id_id = context_data['id_id']
            # context_data['service_user_two'].KOSGU = context_data['KOSGU']
            # context_data['service_user_two'].DopFC = context_data['DopFC']
            # context_data['service_user_two'].budget_planned_old = context_data['budget_planned_old']
            # context_data['service_user_two'].off_budget_planned_old = context_data['off_budget_planned_old']
            # context_data['service_user_two'].budget_planned = context_data['budget_planned']
            # context_data['service_user_two'].off_budget_planned = context_data['off_budget_planned']
            # context_data['service_user_two'].budget_concluded = context_data['budget_concluded']
            # context_data['service_user_two'].off_budget_concluded = context_data['off_budget_concluded']
            # context_data['service_user_two'].budget_remainder = context_data['budget_remainder']
            # context_data['service_user_two'].off_budget_remainder = context_data['off_budget_remainder']
            # context_data['service_user_two'].color = context_data['color']

            fields_to_copy = [
                'id_id', 'KOSGU', 'DopFC', 'budget_planned_old', 'off_budget_planned_old',
                'budget_planned', 'off_budget_planned',
                'budget_concluded', 'off_budget_concluded',
                'budget_remainder', 'off_budget_remainder', 'color'
            ]

            for field in fields_to_copy:
                setattr(context_data['service_user_two'], field, context_data[field])

            await sync_to_async(context_data['service_user_two'].save)()

            await log_user_action(request.user, f'Отредактировал запись в "План-график" с ID {context_data['id_id']},\Стало: budget_planned: {context_data['budget_planned']}, off_budget_planned: {context_data['off_budget_planned']}')

            processor = ContractProcessor(context_data, request)
            return await processor.process_update_user_two()
        except Services.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Service not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON.'}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)

@csrf_exempt  # Необходимо, если вы не используете CSRF-токены
async def add_record(request):
    if request.method == 'POST':
        try:
            # Возвращаем данные формы обратно в шаблон
            context_data = {
                # 'name': request.POST['name'],
                # 'status': request.POST['status'],
                # 'way': request.POST['way'],
                # 'initiator': request.POST['initiator'],
                # 'KTSSR': request.POST['KTSSR'],
                # 'KOSGU': request.POST['KOSGU'],
                # 'DopFC': request.POST['DopFC'],
                # 'NMCC': request.POST['NMCC'],
                # 'counterparty': request.POST['counterparty'],
                # 'registration_number': request.POST['registration_number'],
                # 'contract_number': request.POST['contract_number'],
                # 'contract_date': request.POST['contract_date'],
                # 'end_date': request.POST['end_date'],
                # 'contract_price': request.POST['contract_price'],
                # 'january_one': request.POST['january_one'],
                # 'february': request.POST['february'],
                # 'march': request.POST['march'],
                # 'april': request.POST['april'],
                # 'may': request.POST['may'],
                # 'june': request.POST['june'],
                # 'july': request.POST['july'],
                # 'august': request.POST['august'],
                # 'september': request.POST['september'],
                # 'october': request.POST['october'],
                # 'november': request.POST['november'],
                # 'december': request.POST['december'],
                # 'january_two': request.POST['january_two'],
                # 'date_january_one': request.POST['date_january_one'],
                # 'sum_january_one': request.POST['sum_january_one'],
                # 'date_february': request.POST['date_february'],
                # 'sum_february': request.POST['sum_february'],
                # 'date_march': request.POST['date_march'],
                # 'sum_march':  request.POST['sum_march'],
                # 'date_april': request.POST['date_april'],
                # 'sum_april': request.POST['sum_april'],
                # 'date_may': request.POST['date_may'],
                # 'sum_may': request.POST['sum_may'],
                # 'date_june': request.POST['date_june'],
                # 'sum_june': request.POST['sum_june'],
                # 'date_july': request.POST['date_july'],
                # 'sum_july': request.POST['sum_july'],
                # 'date_august': request.POST['date_august'],
                # 'sum_august': request.POST['sum_august'],
                # 'date_september': request.POST['date_september'],
                # 'sum_september': request.POST['sum_september'],
                # 'date_october': request.POST['date_october'],
                # 'sum_october': request.POST['sum_october'],
                # 'date_november': request.POST['date_november'],
                # 'sum_november': request.POST['sum_november'],
                # 'date_december': request.POST['date_december'],
                # 'sum_december': request.POST['sum_december'],
                # 'date_january_two': request.POST['date_january_two'],
                # 'sum_january_two': request.POST['sum_january_two'],
                # 'execution': request.POST['execution'],
                # 'contract_balance': request.POST['contract_balance'],
                # 'execution_contract_fact': request.POST['execution_contract_fact'],
                # 'execution_contract_plan': request.POST['execution_contract_plan'],
                # 'saving': request.POST['saving'],
                # 'color': request.POST['color'],

                'page': int(request.GET.get('page', '1')) if request.GET.get('page', '1').strip() else 1,
                'page_user': 1,
                'page_user_two': 1,
                'connection_websocket': settings.DATABASES['default']['HOST'],
                'statuses': json.dumps(json_object['statuses']),

                # 'keyword_one': request.GET.get('keyword_one', None),
                # 'keyword_two': request.GET.get('keyword_two', None),
                # 'selected_column_one': request.GET.get('selected_column_one', None),
                # 'selected_column_two': request.GET.get('selected_column_two', None),
                # 'KOSGU_user': request.GET.get('KOSGU_user', None),
                # 'keyword_one_user': request.GET.get('keyword_one_user', None),
                # 'keyword_two_user': request.GET.get('keyword_two_user', None),
                # 'selected_column_one_user': request.GET.get('selected_column_one_user', None),
                # 'selected_column_two_user': request.GET.get('selected_column_two_user', None),
                # 'KOSGU_user_two': request.GET.get('KOSGU_user_two', None),
                # 'keyword_one_user_two': request.GET.get('keyword_one_user_two', None),
                # 'keyword_two_user_two': request.GET.get('keyword_two_user_two', None),
                # 'selected_column_one_user_two': request.GET.get('selected_column_one_user_two', None),
                # 'selected_column_two_user_two': request.GET.get('selected_column_two_user_two', None)
            }

            params = [
                'keyword_one', 'keyword_two', 'keyword_three', 'keyword_four',
                'selected_column_one', 'selected_column_two',
                'contract_date', 'selected_end_date',
                # 'KOSGU_user',
                # 'keyword_one_user', 'keyword_two_user',
                # 'selected_column_one_user', 'selected_column_two_user',
                # 'KOSGU_user_two',
                # 'keyword_one_user_two', 'keyword_two_user_two',
                # 'selected_column_one_user_two', 'selected_column_two_user_two',
            ]

            params_post = [
                'name', 'status', 'way', 'initiator', 'KTSSR',
                'KOSGU', 'DopFC', 'NMCC', 'counterparty',
                'registration_number', 'contract_number', 'contract_date',
                'end_date', 'contract_price', 'january_one',
                'february', 'march', 'april', 'may', 'june', 'july',
                'august', 'september', 'october', 'november', 'december',
                'january_two', 'date_january_one', 'sum_january_one',
                'date_february', 'sum_february', 'date_march', 'sum_march',
                'date_april', 'sum_april', 'date_may', 'sum_may',
                'date_june', 'sum_june', 'date_july', 'sum_july',
                'date_august', 'sum_august', 'date_september', 'sum_september',
                'date_october', 'sum_october', 'date_november', 'sum_november',
                'date_december', 'sum_december', 'date_january_two', 'sum_january_two',
                'execution', 'contract_balance', 'execution_contract_fact', 'execution_contract_plan',
                'saving', 'color', 'remainder_old_year', 'paid_last_year'
            ]

            for param in params:
                context_data[param] = request.GET.get(param, None)

            for param in params_post:
                context_data[param] = request.POST.get(param, None)

            # print('NEVEROV_NEVEROV', context_data)

            processor = ContractProcessor(context_data, request)
            return await processor.process_add()
        except Services.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Service not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON.'}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)

@csrf_exempt  # Необходимо, если вы не используете CSRF-токены
async def add_record_two(request):
    if request.method == 'POST':
        try:
            # Возвращаем данные формы обратно в шаблон
            context_data = {
                # 'name': request.POST['name'],
                # 'KOSGU': request.POST['KOSGU'],
                # 'DopFC': request.POST['DopFC'],

                # 'budget_limit': request.POST['budget_limit'],
                # 'off_budget_limit': request.POST['off_budget_limit'],
                # 'budget_planned': request.POST['budget_planned'],
                # 'off_budget_planned': request.POST['off_budget_planned'],
                # 'budget_bargaining': request.POST['budget_bargaining'],
                # 'off_budget_bargaining': request.POST['off_budget_bargaining'],
                # 'budget_concluded': request.POST['budget_concluded'],
                # 'off_budget_concluded': request.POST['off_budget_concluded'],
                # 'budget_completed': request.POST['budget_completed'],
                # 'off_budget_completed': request.POST['off_budget_completed'],
                # 'budget_execution': request.POST['budget_execution'],
                # 'off_budget_execution': request.POST['off_budget_execution'],
                # 'budget_remainder': request.POST['budget_remainder'],
                # 'off_budget_remainder': request.POST['off_budget_remainder'],
                # 'budget_plans': request.POST['budget_plans'],
                # 'off_budget_plans': request.POST['off_budget_plans'],
                # 'color': request.POST['color'],
                'page': int(request.GET.get('page', '1')) if request.GET.get('page', '1').strip() else 1,
                'page_user': 1,
                'page_user_two': 1,

                # 'keyword_one': request.GET.get('keyword_one', None),
                # 'keyword_two': request.GET.get('keyword_two', None),
                # 'selected_column_one': request.GET.get('selected_column_one', None),
                # 'selected_column_two': request.GET.get('selected_column_two', None),
                # 'KOSGU_user': request.GET.get('KOSGU_user', None),
                # 'keyword_one_user': request.GET.get('keyword_one_user', None),
                # 'keyword_two_user': request.GET.get('keyword_two_user', None),
                # 'selected_column_one_user': request.GET.get('selected_column_one_user', None),
                # 'selected_column_two_user': request.GET.get('selected_column_two_user', None),
                # 'KOSGU_user_two': request.GET.get('KOSGU_user_two', None),
                # 'keyword_one_user_two': request.GET.get('keyword_one_user_two', None),
                # 'keyword_two_user_two': request.GET.get('keyword_two_user_two', None),
                # 'selected_column_one_user_two': request.GET.get('selected_column_one_user_two', None),
                # 'selected_column_two_user_two': request.GET.get('selected_column_two_user_two', None)
            }

            params = [
                'keyword_one', 'keyword_two', 'keyword_three', 'keyword_four',
                'selected_column_one', 'selected_column_two',
                'contract_date', 'selected_end_date',
                # 'KOSGU_user',
                # 'keyword_one_user', 'keyword_two_user',
                # 'selected_column_one_user', 'selected_column_two_user',
                # 'KOSGU_user_two',
                # 'keyword_one_user_two', 'keyword_two_user_two',
                # 'selected_column_one_user_two', 'selected_column_two_user_two',
            ]

            params_post = [
                'name', 'KOSGU', 'DopFC',
            ]

            for param in params:
                context_data[param] = request.GET.get(param, None)

            for param in params_post:
                context_data[param] = request.POST.get(param, None)

            processor = ContractProcessor(context_data, request)
            return await processor.process_add_two()
        except Services.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Service not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON.'}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)

@group_required('Администратор', 'Полный')
@csrf_exempt  # Необходимо, если вы не используете CSRF-токены
async def delete_record(request):
    if request.method == 'POST':
        try:
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
            row_id = body_data.get('id')
            # Найдите запись по ID и обновите цвет
            service = await sync_to_async(Services.objects.get, thread_sensitive=True)(id=row_id)

            # Возвращаем данные формы обратно в шаблон
            context_data = {
                'KOSGU': service.KOSGU,
                'DopFC': service.DopFC,
                'KTSSR': service.KTSSR,
                'status': service.status,
                # 'page': int(request.GET.get('page', '1')) if request.GET.get('page', '1').strip() else 1,
                'page': int(body_data.get('page', '1')),
                'page_user': 1,
                'page_user_two': 1,
                'connection_websocket': settings.DATABASES['default']['HOST'],
                'statuses': json.dumps(json_object['statuses']),

                # 'keyword_one': request.GET.get('keyword_one', None),
                # 'keyword_two': request.GET.get('keyword_two', None),
                # 'selected_column_one': request.GET.get('selected_column_one', None),
                # 'selected_column_two': request.GET.get('selected_column_two', None),
                # 'KOSGU_user': request.GET.get('KOSGU_user', None),
                # 'keyword_one_user': request.GET.get('keyword_one_user', None),
                # 'keyword_two_user': request.GET.get('keyword_two_user', None),
                # 'selected_column_one_user': request.GET.get('selected_column_one_user', None),
                # 'selected_column_two_user': request.GET.get('selected_column_two_user', None),
                # 'KOSGU_user_two': request.GET.get('KOSGU_user_two', None),
                # 'keyword_one_user_two': request.GET.get('keyword_one_user_two', None),
                # 'keyword_two_user_two': request.GET.get('keyword_two_user_two', None),
                # 'selected_column_one_user_two': request.GET.get('selected_column_one_user_two', None),
                # 'selected_column_two_user_two': request.GET.get('selected_column_two_user_two', None)
            }

            params = [
                'keyword_one', 'keyword_two', 'keyword_three', 'keyword_four',
                'selected_column_one', 'selected_column_two',
                'contract_date', 'selected_end_date',
                # 'KOSGU_user',
                # 'keyword_one_user', 'keyword_two_user',
                # 'selected_column_one_user', 'selected_column_two_user',
                # 'KOSGU_user_two',
                # 'keyword_one_user_two','keyword_two_user_two',
                # 'selected_column_one_user_two', 'selected_column_two_user_two',
            ]

            for param in params:
                context_data[param] = body_data.get(param, None)

            # print('---------------------------------------')
            # print(body_data)
            # print('---------------------------------------')

            # Удаляем объект
            await sync_to_async(service.delete, thread_sensitive=True)()

            from django.forms.models import model_to_dict
            service_dict = model_to_dict(service)

            await log_user_action(request.user, f'Удалил запись из "Закупки": {service_dict}')

            processor = ContractProcessor(context_data, request)
            await processor.process_delete()
            return JsonResponse({'success': True}, status=200)
        except Services.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Service not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON.'}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)

@group_required('Администратор', 'Полный')
@csrf_exempt  # Необходимо, если вы не используете CSRF-токены
async def delete_record_two(request):
    if request.method == 'POST':
        try:
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
            row_id = body_data.get('id')
            # Найдите запись по ID и обновите цвет
            service_two = await sync_to_async(Services_Two.objects.get, thread_sensitive=True)(id=row_id)
            # service_three = await sync_to_async(Services_Three.objects.get, thread_sensitive=True)(KOSGU=service_two.KOSGU, DopFC=service_two.DopFC)

            # Удаляем все записи из Services_Three по KOSGU и DopFC из Services_Two
            await sync_to_async(
                lambda: Services_Three.objects.filter(
                    KOSGU=service_two.KOSGU,
                    DopFC=service_two.DopFC
                ).delete(),
                thread_sensitive=True
            )()

            # Возвращаем данные формы обратно в шаблон
            context_data = {
                'KOSGU': service_two.KOSGU,
                'DopFC': service_two.DopFC,
                # 'page': int(request.GET.get('page', '1')) if request.GET.get('page', '1').strip() else 1,
                'page': int(body_data.get('page', '1')),
                'page_user': 1,
                'page_user_two': 1,
                'connection_websocket': settings.DATABASES['default']['HOST'],
                'statuses': json.dumps(json_object['statuses']),

                # 'keyword_one': request.GET.get('keyword_one', None),
                # 'keyword_two': request.GET.get('keyword_two', None),
                # 'selected_column_one': request.GET.get('selected_column_one', None),
                # 'selected_column_two': request.GET.get('selected_column_two', None),
                # 'KOSGU_user': request.GET.get('KOSGU_user', None),
                # 'keyword_one_user': request.GET.get('keyword_one_user', None),
                # 'keyword_two_user': request.GET.get('keyword_two_user', None),
                # 'selected_column_one_user': request.GET.get('selected_column_one_user', None),
                # 'selected_column_two_user': request.GET.get('selected_column_two_user', None),
                # 'KOSGU_user_two': request.GET.get('KOSGU_user_two', None),
                # 'keyword_one_user_two': request.GET.get('keyword_one_user_two', None),
                # 'keyword_two_user_two': request.GET.get('keyword_two_user_two', None),
                # 'selected_column_one_user_two': request.GET.get('selected_column_one_user_two', None),
                # 'selected_column_two_user_two': request.GET.get('selected_column_two_user_two', None)
            }

            params = [
                'keyword_one', 'keyword_two', 'keyword_three', 'keyword_four',
                'selected_column_one', 'selected_column_two',
                'contract_date', 'selected_end_date',
                # 'KOSGU_user',
                # 'keyword_one_user', 'keyword_two_user',
                # 'selected_column_one_user', 'selected_column_two_user',
                # 'KOSGU_user_two',
                # 'keyword_one_user_two', 'keyword_two_user_two',
                # 'selected_column_one_user_two', 'selected_column_two_user_two',
            ]

            for param in params:
                context_data[param] = body_data.get(param, None)

            # Удаляем объект
            await sync_to_async(service_two.delete, thread_sensitive=True)()

            from django.forms.models import model_to_dict
            service_dict = model_to_dict(service_two)

            await log_user_action(request.user, f'Удалил запись из "Свод": {service_dict}')

            processor = ContractProcessor(context_data, request)
            await processor.process_delete_two()
            return JsonResponse({'success': True}, status=200)
        except Services.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Service not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON.'}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)

from .upload_file import upload_file_

@group_required('Администратор', 'Полный')
@csrf_exempt  # Если используете fetch, нужно отключить CSRF или передавать токен
async def upload_file(request):
    return await upload_file_(request)

from django.http import FileResponse, Http404

def download_file(request, filename):
    # Получаем путь к папке "file" внутри вашего проекта
    file_directory = os.path.join(settings.BASE_DIR, 'async_mysql_project', 'file')

    # Строим полный путь к файлу
    file_path = os.path.join(file_directory, filename)

    print(f"Ищем файл по пути: {file_path}")

    # Проверяем, существует ли файл
    if os.path.exists(file_path):
        # Отправляем файл в ответ с помощью FileResponse
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)
    else:
        # Если файл не найден, возвращаем ошибку 404
        raise Http404("Файл не найден")

# Асинхронная функция для копирования данных
@sync_to_async
def copy_service_to_model(service):
    fields = {f.name: getattr(service, f.name) for f in service._meta.fields if f.name != 'id'}
    return fields  # Возвращаем данные для bulk_create

# Асинхронная функция для резервного копирования из Services_backup_one в Services
@group_required('Администратор', 'Полный')
async def backup_to_backup_one(request):
    try:
        # Удаляем все записи в таблице Services (синхронно)
        await sync_to_async(Services.objects.all().delete, thread_sensitive=True)()

        # Получаем данные из Services_backup_one (синхронно через sync_to_async)
        services_backup = await sync_to_async(lambda: list(Services_backup_one.objects.all()))()

        # Копируем данные для вставки в Services
        services_to_create = await asyncio.gather(
            *[copy_service_to_model(service) for service in services_backup]
        )

        # Выполняем bulk_create с помощью sync_to_async
        await sync_to_async(Services.objects.bulk_create)([Services(**fields) for fields in services_to_create])

        processor = ContractProcessor(request)
        await processor.count_dates(False)

        await log_user_action(request.user, 'Резервное копирование в Services из Services_backup_one завершено!')
        return JsonResponse({'success': True})
    except Exception as e:
        errors(e)
        await log_user_action(request.user, f'Ошибка при резервном копировании: {str(e)}')
        return JsonResponse({'success': False, 'message': f'Произошла ошибка при копировании данных: {str(e)}'})

# Асинхронная функция для резервного копирования из Services_backup_two в Services
@group_required('Администратор', 'Полный')
async def backup_to_backup_two(request):
    try:
        # Удаляем все записи в таблице Services (синхронно)
        await sync_to_async(Services.objects.all().delete, thread_sensitive=True)()

        # Получаем данные из Services_backup_two (синхронно через sync_to_async)
        services_backup = await sync_to_async(lambda: list(Services_backup_two.objects.all()))()

        # Копируем данные для вставки в Services
        services_to_create = await asyncio.gather(
            *[copy_service_to_model(service) for service in services_backup]
        )

        # Выполняем bulk_create с помощью sync_to_async
        await sync_to_async(Services.objects.bulk_create)([Services(**fields) for fields in services_to_create])

        processor = ContractProcessor(request)
        await processor.count_dates(False)

        await log_user_action(request.user, 'Резервное копирование в Services из Services_backup_two завершено!')
        return JsonResponse({'success': True})
    except Exception as e:
        errors(e)
        await log_user_action(request.user, f'Ошибка при резервном копировании: {str(e)}')
        return JsonResponse({'success': False, 'message': f'Произошла ошибка при копировании данных: {str(e)}'})