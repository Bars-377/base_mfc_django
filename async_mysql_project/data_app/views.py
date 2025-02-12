from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Services, Services_Two, Services_Three
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator
from django.shortcuts import render
import re
from django.db.models import Sum
from asgiref.sync import sync_to_async

import asyncio

# async def clean_number(value):
#     try:
#         if isinstance(value, (int, float)):
#             return float(value)  # Уже число, возвращаем как есть
#         if not value or value.strip() == '' or value == 'None':
#             return 0.0  # Пустая строка обрабатывается как 0.0
#         return float(value.replace(' ', '').replace(',', '.'))
#     except ValueError:
#         return 0.0  # Пустая строка обрабатывается как 0.0

async def clean_number(value):
    if isinstance(value, (int, float)):
        return float(value)  # Уже число, возвращаем как есть
    if not value or value.strip() == '' or value == 'None':
        return 0.0  # Пустая строка обрабатывается как 0.0
    return float(value.replace(' ', '').replace(',', '.'))

async def skeleton(request, user, contract_date, end_date, keyword_one, keyword_two, selected_column_one, selected_column_two, page, KOSGU_user, keyword_one_user, keyword_two_user, selected_column_one_user, selected_column_two_user, page_user, KOSGU_user_two, keyword_one_user_two, keyword_two_user_two, selected_column_one_user_two, selected_column_two_user_two, page_user_two):
    # contract_date = None if contract_date == 'None' else contract_date
    # end_date = None if end_date == 'None' else end_date
    keyword_one = None if keyword_one == 'None' else keyword_one
    keyword_two = None if keyword_two == 'None' else keyword_two
    selected_column_one = None if selected_column_one == 'None' else selected_column_one
    selected_column_two = None if selected_column_two == 'None' else selected_column_two

    KOSGU_user = None if KOSGU_user == 'None' else KOSGU_user
    keyword_one_user = None if keyword_one_user == 'None' else keyword_one_user
    keyword_two_user = None if keyword_two_user == 'None' else keyword_two_user
    selected_column_one_user = None if selected_column_one_user == 'None' else selected_column_one_user
    selected_column_two_user = None if selected_column_two_user == 'None' else selected_column_two_user

    KOSGU_user_two = None if KOSGU_user_two == 'None' else KOSGU_user_two
    keyword_one_user_two = None if keyword_one_user_two == 'None' else keyword_one_user_two
    keyword_two_user_two = None if keyword_two_user_two == 'None' else keyword_two_user_two
    selected_column_one_user_two = None if selected_column_one_user_two == 'None' else selected_column_one_user_two
    selected_column_two_user_two = None if selected_column_two_user_two == 'None' else selected_column_two_user_two

    per_page = 20

    # Получаем все уникальные значения year и date_number_no_one
    all_years = await sync_to_async(lambda: list(Services.objects.values('contract_date').distinct()))()
    all_end_date = await sync_to_async(lambda: list(Services.objects.values('end_date').distinct()))()
    all_KOSGU_user = await sync_to_async(lambda: list(Services_Two.objects.values('KOSGU').distinct()))()
    all_KOSGU_user_two = await sync_to_async(lambda: list(Services_Three.objects.values('KOSGU').distinct()))()

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

        service_data = await sync_to_async(sorted)({str(int(year)) for year in service_data if year.isdigit()})
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

        service_data = await sync_to_async(sorted)({str(int(year)) for year in service_data if year.isdigit()})
        if empty_found:
            service_data.insert(0, 'None')
        return service_data

    service_years = await process_service_data(all_years, 'contract_date')
    service_end_date = await process_service_data(all_end_date, 'end_date')
    service_KOSGU_user = await process_service_KOSGU(all_KOSGU_user, 'KOSGU')
    service_KOSGU_user_two = await process_service_KOSGU(all_KOSGU_user_two, 'KOSGU')

    # Построение запроса
    query = await sync_to_async(lambda: Services.objects.all())()
    query_user = await sync_to_async(lambda: Services_Two.objects.all())()
    query_user_two = await sync_to_async(lambda: Services_Three.objects.all())()

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

    if KOSGU_user == 'No':
        KOSGU_user = None

    if KOSGU_user_two == 'No':
        KOSGU_user_two = None

    if KOSGU_user == 'None':
        query_user = await sync_to_async(query_user.exclude)(Q(KOSGU__regex=pattern_dd_mm_yyyy) | Q(KOSGU__regex=pattern_yyyy_mm_dd))
    elif KOSGU_user:
        query_user = await sync_to_async(query_user.filter)(KOSGU__icontains=KOSGU_user)

    if KOSGU_user_two == 'None':
        query_user_two = await sync_to_async(query_user_two.exclude)(Q(KOSGU__regex=pattern_dd_mm_yyyy) | Q(KOSGU__regex=pattern_yyyy_mm_dd))
    elif KOSGU_user_two:
        query_user_two = await sync_to_async(query_user_two.filter)(KOSGU__icontains=KOSGU_user_two)

    async def apply_keyword_filter(query, keyword, column, model):
        if keyword:
            if column and hasattr(model, column):
                query = await sync_to_async(query.filter)(**{column + '__icontains': keyword})
            else:
                filters = Q()
                for field in await sync_to_async(model._meta.get_fields)():
                    filters |= Q(**{field.name + '__icontains': keyword})
                query = await sync_to_async(query.filter)(filters)
        return query

    query = await apply_keyword_filter(query, keyword_one, selected_column_one, Services)
    query = await apply_keyword_filter(query, keyword_two, selected_column_two, Services)
    query_user = await apply_keyword_filter(query_user, keyword_one_user, selected_column_one_user, Services_Two)
    query_user = await apply_keyword_filter(query_user, keyword_two_user, selected_column_two_user, Services_Two)
    query_user_two = await apply_keyword_filter(query_user_two, keyword_one_user_two, selected_column_one_user_two, Services_Three)
    query_user_two = await apply_keyword_filter(query_user_two, keyword_two_user_two, selected_column_two_user_two, Services_Three)

    # Сортировка
    from django.db.models import IntegerField, DateField
    from django.db.models.functions import Cast

    # Преобразование id_id в целое число и contract_date в дату перед сортировкой
    query = query.annotate(
        id_id_int=Cast('id_id', IntegerField()),
        contract_date_date=Cast('contract_date', DateField())
    ).order_by('id_id_int', 'contract_date_date')

    # Преобразование id_id в целое число и contract_date в дату перед сортировкой
    query_user = query_user.annotate(
        id_id_int=Cast('id_id', IntegerField())
    ).order_by('id_id_int')

    # Преобразование id_id в целое число и contract_date в дату перед сортировкой
    query_user_two = query_user_two.annotate(
        id_id_int=Cast('id_id', IntegerField())
    ).order_by('id_id_int')

    # # Логика подсчета стоимости
    total_cost_1 = await sync_to_async(lambda: query_user.aggregate(Sum('budget_limit')))()
    total_cost_1 = total_cost_1['budget_limit__sum'] or 0
    total_cost_2 = await sync_to_async(lambda: query_user.aggregate(Sum('off_budget_limit')))()
    total_cost_2 = total_cost_2['off_budget_limit__sum'] or 0
    total_cost_3 = await sync_to_async(lambda: query_user.aggregate(Sum('budget_planned')))()
    total_cost_3 = total_cost_3['budget_planned__sum'] or 0
    total_cost_4 = await sync_to_async(lambda: query_user.aggregate(Sum('off_budget_planned')))()
    total_cost_4 = total_cost_4['off_budget_planned__sum'] or 0
    total_cost_5 = await sync_to_async(lambda: query_user.aggregate(Sum('budget_bargaining')))()
    total_cost_5 = total_cost_5['budget_bargaining__sum'] or 0
    total_cost_6 = await sync_to_async(lambda: query_user.aggregate(Sum('off_budget_bargaining')))()
    total_cost_6 = total_cost_6['off_budget_bargaining__sum'] or 0
    total_cost_7 = await sync_to_async(lambda: query_user.aggregate(Sum('budget_concluded')))()
    total_cost_7 = total_cost_7['budget_concluded__sum'] or 0
    total_cost_8 = await sync_to_async(lambda: query_user.aggregate(Sum('off_budget_concluded')))()
    total_cost_8 = total_cost_8['off_budget_concluded__sum'] or 0
    total_cost_9 = await sync_to_async(lambda: query_user.aggregate(Sum('budget_completed')))()
    total_cost_9 = total_cost_9['budget_completed__sum'] or 0
    total_cost_10 = await sync_to_async(lambda: query_user.aggregate(Sum('off_budget_completed')))()
    total_cost_10 = total_cost_10['off_budget_completed__sum'] or 0
    total_cost_11 = await sync_to_async(lambda: query_user.aggregate(Sum('budget_execution')))()
    total_cost_11 = total_cost_11['budget_execution__sum'] or 0
    total_cost_12 = await sync_to_async(lambda: query_user.aggregate(Sum('off_budget_execution')))()
    total_cost_12 = total_cost_12['off_budget_execution__sum'] or 0
    total_cost_13 = await sync_to_async(lambda: query_user.aggregate(Sum('budget_remainder')))()
    total_cost_13 = total_cost_13['budget_remainder__sum'] or 0
    total_cost_14 = await sync_to_async(lambda: query_user.aggregate(Sum('off_budget_remainder')))()
    total_cost_14 = total_cost_14['off_budget_remainder__sum'] or 0
    total_cost_15 = await sync_to_async(lambda: query_user.aggregate(Sum('budget_plans')))()
    total_cost_15 = total_cost_15['budget_plans__sum'] or 0
    total_cost_16 = await sync_to_async(lambda: query_user.aggregate(Sum('off_budget_plans')))()
    total_cost_16 = total_cost_16['off_budget_plans__sum'] or 0

    try:
        total_cost_17 = total_cost_1 + total_cost_2
        total_cost_18 = ((total_cost_11 + total_cost_12) / total_cost_17) * 100
        total_cost_18 = round(total_cost_18, 2)  # Округляем до двух знаков после запятой
    except:
        total_cost_17 = 0
        total_cost_18 = 0.00

    # Получаем все записи из таблицы Services_Three
    Services_Three_ = await sync_to_async(list)(Services_Three.objects.all())
    total_cost_1_1 = 0
    total_cost_1_2 = 0
    total_cost_1_3 = 0
    total_cost_1_4 = 0
    total_cost_1_5 = 0
    total_cost_1_6 = 0
    for service in Services_Three_:
        total_cost_1_1 += await clean_number(service.budget_planned)
        total_cost_1_2 += await clean_number(service.off_budget_planned)
        total_cost_1_3 += await clean_number(service.budget_concluded)
        total_cost_1_4 += await clean_number(service.off_budget_concluded)
        total_cost_1_5 += await clean_number(service.budget_remainder)
        total_cost_1_6 += await clean_number(service.off_budget_remainder)

    total_cost_1_7 = total_cost_17 - (total_cost_1_3 + total_cost_1_4)

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
        'total_cost_1': total_cost_1,
        'total_cost_2': total_cost_2,
        'total_cost_3': total_cost_3,
        'total_cost_4': total_cost_4,
        'total_cost_5': total_cost_5,
        'total_cost_6': total_cost_6,
        'total_cost_7': total_cost_7,
        'total_cost_8': total_cost_8,
        'total_cost_9': total_cost_9,
        'total_cost_10': total_cost_10,
        'total_cost_11': total_cost_11,
        'total_cost_12': total_cost_12,
        'total_cost_13': total_cost_13,
        'total_cost_14': total_cost_14,
        'total_cost_15': total_cost_15,
        'total_cost_16': total_cost_16,
        'total_cost_17': total_cost_17,
        'total_cost_18': total_cost_18,
        'total_cost_1_1': total_cost_1_1,
        'total_cost_1_2': total_cost_1_2,
        'total_cost_1_3': total_cost_1_3,
        'total_cost_1_4': total_cost_1_4,
        'total_cost_1_5': total_cost_1_5,
        'total_cost_1_6': total_cost_1_6,
        'total_cost_1_7': total_cost_1_7,
        'selected_contract_date': contract_date,
        'selected_KOSGU_user': KOSGU_user,
        'selected_KOSGU_user_two': KOSGU_user_two,
        'selected_end_date': end_date,
        'selected_column_one': selected_column_one,
        'selected_column_one_user': selected_column_one_user,
        'selected_column_one_user_two': selected_column_one_user_two,
        'selected_column_two': selected_column_two,
        'selected_column_two_user': selected_column_two_user,
        'selected_column_two_user_two': selected_column_two_user_two,
        'keyword_one': keyword_one,
        'keyword_one_user': keyword_one_user,
        'keyword_one_user_two': keyword_one_user_two,
        'keyword_two': keyword_two,
        'keyword_two_user': keyword_two_user,
        'keyword_two_user_two': keyword_two_user_two,
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
        'service_KOSGU_user': service_KOSGU_user,
        'service_KOSGU_user_two': service_KOSGU_user_two,
        'service_end_date': service_end_date
    }

    return await sync_to_async(render)(request, 'data_table.html', context)

from asgiref.sync import sync_to_async

@login_required
async def data_table_view(request):
    user = request.user

    total_pages_full = request.GET.get('total_pages_full', None)

    if total_pages_full:
        per_page = 20

        query = await sync_to_async(lambda: Services.objects.all())()

        total_services_full = await sync_to_async(lambda: query.count())()
        page = (total_services_full + per_page - 1) // per_page
    else:
        page = int(request.GET.get('page', 1))

    contract_date = request.GET.get('contract_date', None)
    end_date = request.GET.get('end_date', None)
    keyword_one = request.GET.get('keyword_one', None)
    keyword_two = request.GET.get('keyword_two', None)
    selected_column_one = request.GET.get('selected_column_one', None)
    selected_column_two = request.GET.get('selected_column_two', None)

    total_pages_full_user = request.GET.get('total_pages_full_user', None)

    if total_pages_full_user:
        per_page = 20

        query_user = await sync_to_async(lambda: Services_Two.objects.all())()

        total_services_full_user = await sync_to_async(lambda: query_user.count())()
        page_user = (total_services_full_user + per_page - 1) // per_page
    else:
        page_user = int(request.GET.get('page_user', 1))

    total_pages_full_user_two = request.GET.get('total_pages_full_user_two', None)

    if total_pages_full_user_two:
        per_page = 20

        query_user_two = await sync_to_async(lambda: Services_Three.objects.all())()

        total_services_full_user_two = await sync_to_async(lambda: query_user_two.count())()
        page_user_two = (total_services_full_user_two + per_page - 1) // per_page
    else:
        page_user_two = int(request.GET.get('page_user_two', 1))

    KOSGU_user = request.GET.get('KOSGU_user', None)
    keyword_one_user = request.GET.get('keyword_one_user', None)
    keyword_two_user = request.GET.get('keyword_two_user', None)
    selected_column_one_user = request.GET.get('selected_column_one_user', None)
    selected_column_two_user = request.GET.get('selected_column_two_user', None)

    KOSGU_user_two = request.GET.get('KOSGU_user_two', None)
    keyword_one_user_two = request.GET.get('keyword_one_user_two', None)
    keyword_two_user_two = request.GET.get('keyword_two_user_two', None)
    selected_column_one_user_two = request.GET.get('selected_column_one_user_two', None)
    selected_column_two_user_two = request.GET.get('selected_column_two_user_two', None)

    return await skeleton(request, user, contract_date, end_date, keyword_one, keyword_two, selected_column_one, selected_column_two, page, KOSGU_user, keyword_one_user, keyword_two_user, selected_column_one_user, selected_column_two_user, page_user, KOSGU_user_two, keyword_one_user_two, keyword_two_user_two, selected_column_one_user_two, selected_column_two_user_two, page_user_two)

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User

async def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = await sync_to_async(authenticate)(request, username=username, password=password)
        if user is not None:
            await sync_to_async(login)(request, user)
            return redirect('data_table_view')  # Переход на страницу после успешного входа
        else:
            await sync_to_async(messages.error)(request, "Неверное имя пользователя или пароль")
    return await sync_to_async(render)(request, 'login.html')  # Ваш шаблон для входа

# Асинхронная обертка для создания пользователя
@sync_to_async
def create_user(username, email, password):
    return User.objects.create_user(username=username, email=email, password=password)

async def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            await create_user(username=username, email=email, password=password)
            await sync_to_async(messages.success)(request, "Регистрация прошла успешно. Вы можете войти.")
            return redirect('login')
        else:
            await sync_to_async(messages.error)(request, "Пароли не совпадают")
    return await sync_to_async(render)(request, 'register.html')  # Ваш шаблон для регистрации

@csrf_exempt  # Необходимо, если вы не используете CSRF-токены
async def update_color(request, row_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            color = data.get('color')

            # Найдите запись по ID и обновите цвет
            service = await sync_to_async(Services.objects.get)(id=row_id)
            service.color = color
            await sync_to_async(service.save)()

            return JsonResponse({'success': True, 'id': service.id, 'color': service.color})
        except Services.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Service not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON.'}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)

@csrf_exempt  # Необходимо, если вы не используете CSRF-токены
async def update_color_user(request, row_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            color = data.get('color')

            # Найдите запись по ID и обновите цвет
            service = await sync_to_async(Services_Two.objects.get)(id=row_id)
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
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            color = data.get('color')

            # Найдите запись по ID и обновите цвет
            service = await sync_to_async(Services_Three.objects.get)(id=row_id)
            service.color = color
            await sync_to_async(service.save)()

            return JsonResponse({'success': True, 'id': service.id, 'color': service.color})
        except Services_Two.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Service not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON.'}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)

# from django.shortcuts import get_object_or_404

@csrf_exempt  # Необходимо, если вы не используете CSRF-токены
async def add(request):
    page = int(request.GET.get('page', 1))
    keyword_one = request.GET.get('keyword_one', None)
    keyword_two = request.GET.get('keyword_two', None)
    selected_column_one = request.GET.get('selected_column_one', None)
    selected_column_two = request.GET.get('selected_column_two', None)
    selected_contract_date = request.GET.get('contract_date', "No")
    selected_end_date = request.GET.get('end_date', "No")
    total_pages = int(request.GET.get('total_pages', 1))

    user = request.user

    # Подготовка контекста для шаблона
    context = {
        'user': user,
        'page': page,
        'keyword_one': keyword_one,
        'keyword_two': keyword_two,
        'selected_column_one': selected_column_one,
        'selected_column_two': selected_column_two,
        'selected_contract_date': selected_contract_date,
        'selected_end_date': selected_end_date,
        'total_pages': total_pages
    }

    return await sync_to_async(render)(request, 'add.html', context)

from .admin import admin_required

@admin_required
@csrf_exempt  # Необходимо, если вы не используете CSRF-токены
async def edit(request, row_id):
    # Возвращаем данные формы обратно в шаблон
    context_data = {
        # 'row_id_user': row_id,
        'page': int(request.GET.get('page', '1')) if request.GET.get('page', '1').strip() else 1,
        'keyword_one': request.GET.get('keyword_one', None),
        'keyword_two': request.GET.get('keyword_two', None),
        'selected_column_one': request.GET.get('selected_column_one', None),
        'selected_column_two': request.GET.get('selected_column_two', None),
        'page_user': int(request.GET.get('page_user', '1')) if request.GET.get('page', '1').strip() else 1,
        'KOSGU_user': request.GET.get('KOSGU_user', None),
        'keyword_one_user': request.GET.get('keyword_one_user', None),
        'keyword_two_user': request.GET.get('keyword_two_user', None),
        'selected_column_one_user': request.GET.get('selected_column_one_user', None),
        'selected_column_two_user': request.GET.get('selected_column_two_user', None),
        'page_user_two': int(request.GET.get('page_user_two', '1')) if request.GET.get('page', '1').strip() else 1,
        'KOSGU_user_two': request.GET.get('KOSGU_user_two', None),
        'keyword_one_user_two': request.GET.get('keyword_one_user_two', None),
        'keyword_two_user_two': request.GET.get('keyword_two_user_two', None),
        'selected_column_one_user_two': request.GET.get('selected_column_one_user_two', None),
        'selected_column_two_user_two': request.GET.get('selected_column_two_user_two', None)
    }

    # if user != 12:
    #     await sync_to_async(messages.error)(request, "Редактировать таблицу Закупки может только Администратор")
    #     # Кодируем query-параметры
    #     query_string = urlencode(context_data)

    #     # Формируем URL с query-параметрами
    #     redirect_url = f"{reverse('data_table_view')}?{query_string}"  # Замените 'index' на имя вашего URL-шаблона

    #     # Перенаправляем пользователя
    #     return HttpResponseRedirect(redirect_url)

    page = int(request.GET.get('page', 1))
    keyword_one = request.GET.get('keyword_one', None)
    keyword_two = request.GET.get('keyword_two', None)
    selected_column_one = request.GET.get('selected_column_one', None)
    selected_column_two = request.GET.get('selected_column_two', None)
    selected_contract_date = request.GET.get('contract_date', "No")
    selected_end_date = request.GET.get('end_date', "No")

    # Получаем объект service по id
    service = await sync_to_async(Services.objects.get)(id=row_id)

    # Подготовка контекста для шаблона
    context = {
        'service': service,
        'status': '',
        'way': '',
        'KTSSR': '',
        'KOSGU': '',
        'DopFC': '',
        'row_id': row_id,
        'page': page,
        'keyword_one': keyword_one,
        'keyword_two': keyword_two,
        'selected_column_one': selected_column_one,
        'selected_column_two': selected_column_two,
        'selected_contract_date': selected_contract_date,
        'selected_end_date': selected_end_date
    }

    return await sync_to_async(render)(request, 'edit.html', context)

@admin_required
@csrf_exempt  # Необходимо, если вы не используете CSRF-токены
async def edit_user(request, row_id):
    # Возвращаем данные формы обратно в шаблон
    context_data = {
        # 'row_id_user': row_id,
        'page': int(request.GET.get('page', '1')) if request.GET.get('page', '1').strip() else 1,
        'keyword_one': request.GET.get('keyword_one', None),
        'keyword_two': request.GET.get('keyword_two', None),
        'selected_column_one': request.GET.get('selected_column_one', None),
        'selected_column_two': request.GET.get('selected_column_two', None),
        'page_user': int(request.GET.get('page_user', '1')) if request.GET.get('page', '1').strip() else 1,
        'KOSGU_user': request.GET.get('KOSGU_user', None),
        'keyword_one_user': request.GET.get('keyword_one_user', None),
        'keyword_two_user': request.GET.get('keyword_two_user', None),
        'selected_column_one_user': request.GET.get('selected_column_one_user', None),
        'selected_column_two_user': request.GET.get('selected_column_two_user', None),
        'page_user_two': int(request.GET.get('page_user_two', '1')) if request.GET.get('page', '1').strip() else 1,
        'KOSGU_user_two': request.GET.get('KOSGU_user_two', None),
        'keyword_one_user_two': request.GET.get('keyword_one_user_two', None),
        'keyword_two_user_two': request.GET.get('keyword_two_user_two', None),
        'selected_column_one_user_two': request.GET.get('selected_column_one_user_two', None),
        'selected_column_two_user_two': request.GET.get('selected_column_two_user_two', None)
    }

    # if user != 12:
    #     await sync_to_async(messages.error)(request, "Редактировать таблицу План - график может только Администратор")
    #     # Кодируем query-параметры
    #     query_string = urlencode(context_data)

    #     # Формируем URL с query-параметрами
    #     redirect_url = f"{reverse('data_table_view')}?{query_string}"  # Замените 'index' на имя вашего URL-шаблона

    #     # Перенаправляем пользователя
    #     return HttpResponseRedirect(redirect_url)

    page_user = int(request.GET.get('page_user', 1))
    keyword_one_user = request.GET.get('keyword_one_user', None)
    keyword_two_user = request.GET.get('keyword_two_user', None)
    selected_column_one_user = request.GET.get('selected_column_one_user', None)
    selected_column_two_user = request.GET.get('selected_column_two_user', None)
    selected_contract_date_user = request.GET.get('selected_contract_date_user', "No")
    selected_end_date_user = request.GET.get('selected_end_date_user', "No")

    # Получаем объект service_user по id
    service_user = await sync_to_async(Services_Two.objects.get)(id=row_id)

    # Подготовка контекста для шаблона
    context = {
        'service_user': service_user,
        'row_id_user': row_id,
        'page_user': page_user,
        'keyword_one_user': keyword_one_user,
        'keyword_two_user': keyword_two_user,
        'selected_column_one_user': selected_column_one_user,
        'selected_column_two_user': selected_column_two_user,
        'selected_contract_date_user': selected_contract_date_user,
        'selected_end_date_user': selected_end_date_user
    }

    return await sync_to_async(render)(request, 'edit_user.html', context)

@admin_required
@csrf_exempt  # Необходимо, если вы не используете CSRF-токены
async def edit_user_two(request, row_id):
    # Возвращаем данные формы обратно в шаблон
    context_data = {
        # 'row_id_user': row_id,
        'page': int(request.GET.get('page', '1')) if request.GET.get('page', '1').strip() else 1,
        'keyword_one': request.GET.get('keyword_one', None),
        'keyword_two': request.GET.get('keyword_two', None),
        'selected_column_one': request.GET.get('selected_column_one', None),
        'selected_column_two': request.GET.get('selected_column_two', None),
        'page_user': int(request.GET.get('page_user', '1')) if request.GET.get('page', '1').strip() else 1,
        'KOSGU_user': request.GET.get('KOSGU_user', None),
        'keyword_one_user': request.GET.get('keyword_one_user', None),
        'keyword_two_user': request.GET.get('keyword_two_user', None),
        'selected_column_one_user': request.GET.get('selected_column_one_user', None),
        'selected_column_two_user': request.GET.get('selected_column_two_user', None),
        'page_user_two': int(request.GET.get('page_user_two', '1')) if request.GET.get('page', '1').strip() else 1,
        'KOSGU_user_two': request.GET.get('KOSGU_user_two', None),
        'keyword_one_user_two': request.GET.get('keyword_one_user_two', None),
        'keyword_two_user_two': request.GET.get('keyword_two_user_two', None),
        'selected_column_one_user_two': request.GET.get('selected_column_one_user_two', None),
        'selected_column_two_user_two': request.GET.get('selected_column_two_user_two', None)
    }

    # if user != 12:
    #     await sync_to_async(messages.error)(request, "Редактировать таблицу Свод может только Администратор")
    #     # Кодируем query-параметры
    #     query_string = urlencode(context_data)

    #     # Формируем URL с query-параметрами
    #     redirect_url = f"{reverse('data_table_view')}?{query_string}"  # Замените 'index' на имя вашего URL-шаблона

    #     # Перенаправляем пользователя
    #     return HttpResponseRedirect(redirect_url)

    page_user = int(request.GET.get('page_user', 1))
    keyword_one_user = request.GET.get('keyword_one_user', None)
    keyword_two_user = request.GET.get('keyword_two_user', None)
    selected_column_one_user = request.GET.get('selected_column_one_user', None)
    selected_column_two_user = request.GET.get('selected_column_two_user', None)
    selected_contract_date_user = request.GET.get('selected_contract_date_user', "No")
    selected_end_date_user = request.GET.get('selected_end_date_user', "No")

    # Получаем объект service_user_two по id
    service_user_two = await sync_to_async(Services_Three.objects.get)(id=row_id)

    # Подготовка контекста для шаблона
    context = {
        'service_user_two': service_user_two,
        'row_id_user_two': row_id,
        'page_user': page_user,
        'keyword_one_user': keyword_one_user,
        'keyword_two_user': keyword_two_user,
        'selected_column_one_user': selected_column_one_user,
        'selected_column_two_user': selected_column_two_user,
        'selected_contract_date_user': selected_contract_date_user,
        'selected_end_date_user': selected_end_date_user
    }

    return await sync_to_async(render)(request, 'edit_user_two.html', context)

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

class ContractProcessor:
    def __init__(self, context_data, request):
        self.context_data = context_data
        self.request = request

    async def clean_number_two(self, value):
        # Ваша реализация функции clean_number
        if value in [None, 'None', '']:
            return 0
        return float(value)

    async def validate_execution_plan(self):
        execution_contract_plan = await self.calculate_execution_plan()
        if self.context_data['contract_price']:
            if f"{execution_contract_plan:g}" != self.context_data['contract_price']:
                return False
        return True

    async def validate_execution_plan_message(self):
        await sync_to_async(messages.error)(self.request, 'Значение поля «Исполнение контракта (план) должно равняться полю «Цена контракта»')

    async def validate_execution_fact(self):
        execution_contract_plan = await self.calculate_execution_plan()
        execution_contract_fact = await self.calculate_execution_fact()
        if execution_contract_plan != execution_contract_fact and self.context_data['status'] == 'Исполнено':
            return False
        return True

    async def validate_execution_fact_message(self):
        await sync_to_async(messages.error)(self.request, 'Нельзя выставить статус "Исполнено" при неравенстве ячеек «Исполнение контракта (факт)» и «Исполнение контракта (план)»')

    async def validate_Services_Two(self):
        try:
            from django.db.models import Q

            Services_Two_ = await sync_to_async(Services_Two.objects.get)(
                Q(KOSGU=self.context_data['KOSGU']) & Q(DopFC=self.context_data['DopFC'])
            )
            return Services_Two_
        except:
            return False

    async def validate_Services_Two_message(self):
        await sync_to_async(messages.error)(self.request, 'Нет сопоставления КОСГУ с ДопФК')

    async def validate_Services(self):
        from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

        try:
            Services_ = await sync_to_async(Services.objects.get)(name=self.context_data['name'])
            return False
        except MultipleObjectsReturned:
            Services_ = await sync_to_async(lambda: Services.objects.filter(name=self.context_data['name']).first())()
            return False
        except ObjectDoesNotExist:
            return True

    async def validate_Services_message(self):
        await sync_to_async(messages.error)(self.request, 'Вы добавляете дубликат в Наименовании')

    async def calculate_execution_plan(self):
        months = [self.context_data[month] for month in [
            'january_one', 'february', 'march', 'april', 'may', 'june',
            'july', 'august', 'september', 'october', 'november', 'december',
            'january_two'
        ]]
        cleaned_numbers = await asyncio.gather(*(clean_number(month) for month in months))
        return sum(cleaned_numbers)

    async def calculate_execution_fact(self):
        sum_months = [self.context_data[month] for month in [
            'sum_january_one', 'sum_february', 'sum_march', 'sum_april', 'sum_may', 'sum_june',
            'sum_july', 'sum_august', 'sum_september', 'sum_october', 'sum_november', 'sum_december',
            'sum_january_two'
        ]]
        cleaned_numbers = await asyncio.gather(*(clean_number(month) for month in sum_months))
        return sum(cleaned_numbers)

    async def update_service(self, saving, execution_contract_plan, execution_contract_fact):
        """Подсчёт Исполнение контракта (план) (формула) и Исполнение контракта (факт) (формула)"""
        service = self.context_data['service']

        # Обновляем значения в self.context_data
        self.context_data['saving'] = saving
        self.context_data['execution_contract_plan'] = execution_contract_plan
        self.context_data['execution_contract_fact'] = execution_contract_fact

        for key, value in self.context_data.items():
            setattr(service, key, value)

        await sync_to_async(service.save)()

    async def creation_new_service(self, saving, execution_contract_plan, execution_contract_fact, new_service):
        """Формируем запрос для новой записи"""
        from django.db import connection

        # Получаем следующий ID
        def get_latest_service():
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id_id FROM services
                    WHERE id_id REGEXP '^[0-9]+$'
                    ORDER BY CAST(id_id AS UNSIGNED) DESC
                    LIMIT 1
                """)
                row = cursor.fetchone()
                return row

        latest_service = await sync_to_async(get_latest_service)()

        try:
            id_id = (int(latest_service[0]) + 1) if latest_service and latest_service[0].isdigit() else 1
        except ValueError:
            # В случае некорректного значения установить id_id на 1
            id_id = 1

        contract_balance = await clean_number(self.context_data['contract_price']) - await clean_number(execution_contract_fact)

        # Добавляем id_id в объект new_service
        setattr(new_service, 'id_id', id_id)
        for key, value in self.context_data.items():
            if key == saving:
                setattr(new_service, key, saving)
            elif key == execution_contract_plan:
                setattr(new_service, key, execution_contract_plan)
            elif key == execution_contract_fact:
                setattr(new_service, key, execution_contract_fact)
            else:
                setattr(new_service, key, value)
        # Добавляем contract_balance в объект new_service
        setattr(new_service, 'contract_balance', contract_balance)

        return new_service

    async def calculate_contract_sums(self, KTSSR, status):
        """Получаем сумму всех contract_price либо execution_contract_fact"""
        from django.db.models import Q

        # Общий фильтр для обоих случаев
        filters = Q(KOSGU=self.context_data['KOSGU']) & Q(DopFC=self.context_data['DopFC']) & Q(KTSSR=KTSSR)

        if status:
            filters &= Q(status=status)
            field_to_sum = 'contract_price'
        else:
            field_to_sum = 'execution_contract_fact'

        # Асинхронно выполняем агрегацию
        total_sum = await sync_to_async(self._aggregate_sum)(filters, field_to_sum)

        # Очищаем число, если это необходимо
        return await clean_number(total_sum if total_sum not in [None, 'None', ''] else 0)

    def _aggregate_sum(self, filters, field_to_sum):
        return Services.objects.filter(filters).aggregate(total_sum=Sum(field_to_sum, default=0))['total_sum']

    async def process_budget_services_two(self, Services_Two_):
        """Обновление второй базы"""
        # Создаем список месяцев
        budget = [
            Services_Two_.budget_limit if Services_Two_.budget_limit not in [None, 'None', ''] else 0,
            Services_Two_.budget_bargaining if Services_Two_.budget_bargaining not in [None, 'None', ''] else 0,
            Services_Two_.budget_concluded if Services_Two_.budget_concluded not in [None, 'None', ''] else 0,
            Services_Two_.budget_completed if Services_Two_.budget_completed not in [None, 'None', ''] else 0
        ]

        # Асинхронно обрабатываем все месяцы
        cleaned_numbers = await asyncio.gather(*(clean_number(number) for number in budget))

        # Суммируем результат
        Services_Two_.budget_remainder = cleaned_numbers[0] - sum(cleaned_numbers[1:])

        # Создаем список месяцев
        off_budget = [
            Services_Two_.off_budget_limit if Services_Two_.off_budget_limit not in [None, 'None', ''] else 0,
            Services_Two_.off_budget_bargaining if Services_Two_.off_budget_bargaining not in [None, 'None', ''] else 0,
            Services_Two_.off_budget_concluded if Services_Two_.off_budget_concluded not in [None, 'None', ''] else 0,
            Services_Two_.off_budget_completed if Services_Two_.off_budget_completed not in [None, 'None', ''] else 0
        ]

        # Асинхронно обрабатываем все месяцы
        cleaned_numbers = await asyncio.gather(*(clean_number(number) for number in off_budget))

        # Суммируем результат
        Services_Two_.off_budget_remainder = cleaned_numbers[0] - sum(cleaned_numbers[1:])

        # Расчет планов
        Services_Two_.budget_plans = await self.clean_number_two(Services_Two_.budget_remainder) - await self.clean_number_two(Services_Two_.budget_planned)
        Services_Two_.off_budget_plans = await self.clean_number_two(Services_Two_.off_budget_remainder) - await self.clean_number_two(Services_Two_.off_budget_planned)

        if any(x < 0 for x in [await clean_number(Services_Two_.budget_remainder),
                            await clean_number(Services_Two_.off_budget_remainder)
                            # await clean_number(Services_Two_.budget_plans),
                            # await clean_number(Services_Two_.off_budget_plans)
                            ]):
            Services_Two_.color = '#ffebeb'
        else:
            Services_Two_.color = ''

        await sync_to_async(Services_Two_.save)()

    async def process_budget_services_three(self, contract_price_sum_way, ServicesTwo_):
        """Обновление третьей базы"""
        try:

            from django.db.models import Q

            Services_Three_ = await sync_to_async(Services_Three.objects.get)(
                Q(KOSGU=self.context_data['KOSGU']) & Q(DopFC=self.context_data['DopFC'])
            )

            if contract_price_sum_way:

                try:

                    if self.context_data['status'] == 'Заключено' and self.context_data['KTSSR'] == '2016100092':
                        Services_Three_.off_budget_concluded = contract_price_sum_way if contract_price_sum_way else ServicesTwo_.off_budget_concluded
                        # Services_Three_.off_budget_remainder = await clean_number(ServicesTwo_.off_budget_planned) - await clean_number(contract_price_sum_way)
                    elif self.context_data['status'] == 'Заключено' and self.context_data['KTSSR'] == '2016100000':
                        Services_Three_.budget_concluded = contract_price_sum_way if contract_price_sum_way else ServicesTwo_.budget_concluded
                        # Services_Three_.budget_remainder = await clean_number(ServicesTwo_.budget_planned) - await clean_number(contract_price_sum_way)

                except KeyError:
                    pass

            await sync_to_async(Services_Three_.save)()

            Services_Three_ = await sync_to_async(Services_Three.objects.get)(
                Q(KOSGU=self.context_data['KOSGU']) & Q(DopFC=self.context_data['DopFC'])
            )

            Services_Three_.budget_remainder = await clean_number(Services_Three_.budget_planned) - await clean_number(Services_Three_.budget_concluded)
            Services_Three_.off_budget_remainder = await clean_number(Services_Three_.off_budget_planned) - await clean_number(Services_Three_.off_budget_concluded)

            if any(x < 0 for x in [await clean_number(Services_Three_.budget_remainder),
                                await clean_number(Services_Three_.off_budget_remainder)
                                # await clean_number(Services_Three_.budget_planned),
                                # await clean_number(Services_Three_.off_budget_planned)
                                ]):
                Services_Three_.color = '#ffebeb'
            else:
                Services_Three_.color = ''

            await sync_to_async(Services_Three_.save)()

        except Exception as e:
            # Вывод подробной информации об ошибке
            print(f"Поймано исключение: {type(e).__name__}")
            print(f"Сообщение об ошибке: {str(e)}")
            import traceback
            print("Трассировка стека (stack trace):")
            traceback.print_exc()

    async def message_service_update(self):
        await sync_to_async(messages.success)(self.request, "Редактирование прошло успешно!")

    async def message_service_add(self):
        await sync_to_async(messages.success)(self.request, "Данные успешно добавлены!")

    async def message_service_delete(self):
        await sync_to_async(messages.success)(self.request, "Данные успешно удалены!")

    async def aggregate_fields(self, fields):
        """Суммирование столбцов"""
        results = {}
        for field in fields:
            # Асинхронно выполняем агрегацию по каждому полю
            result = await sync_to_async(lambda: Services_Two.objects.aggregate(**{f'{field}__sum': Sum(field)}))()
            # Получаем значение суммы или 0, если оно None
            results[field] = result[f'{field}__sum'] or 0
        return results

    async def total_costs(self, new_service):
        """Удаление новой записи если условия соответствуют"""
        # Определите список всех полей, которые нужно агрегировать
        fields = [
            'budget_limit',
            'off_budget_limit',
            'budget_planned',
            'off_budget_planned',
            'budget_bargaining',
            'off_budget_bargaining',
            'budget_concluded',
            'off_budget_concluded',
            'budget_completed',
            'off_budget_completed'
        ]

        # Вызов функции для выполнения агрегации
        aggregated_results = await self.aggregate_fields(fields)

        # Теперь вы можете получить значения из aggregated_results
        total_costs_calc = {
        'total_cost_1': aggregated_results['budget_limit'],
        'total_cost_2': aggregated_results['off_budget_limit'],
        'total_cost_3': aggregated_results['budget_planned'],
        'total_cost_4': aggregated_results['off_budget_planned'],
        'total_cost_5': aggregated_results['budget_bargaining'],
        'total_cost_6': aggregated_results['off_budget_bargaining'],
        'total_cost_7': aggregated_results['budget_concluded'],
        'total_cost_8': aggregated_results['off_budget_concluded'],
        'total_cost_9': aggregated_results['budget_completed'],
        'total_cost_10': aggregated_results['off_budget_completed']
        }

        if total_costs_calc['total_cost_1'] < (total_costs_calc['total_cost_3'] or total_costs_calc['total_cost_5'] or total_costs_calc['total_cost_7'] or total_costs_calc['total_cost_9']):
            if new_service:
                await sync_to_async(new_service.delete)()
            return False

        if total_costs_calc['total_cost_2'] < (total_costs_calc['total_cost_4'] or total_costs_calc['total_cost_6'] or total_costs_calc['total_cost_8'] or total_costs_calc['total_cost_10']):
            if new_service:
                await sync_to_async(new_service.delete)()
            return False
        return True

    async def total_costs_message(self):
        await sync_to_async(messages.error)(self.request, 'Запрещено вносить новую строку, если после ее ввода сумма контрактов по соответствующему КЦСР, КОСГУ и ДопФК превысит значение поля «Лимиты»')

    async def Services_way(self, KTSSR, status):
        """Подсчёт Цена контракта (на 2024 год) и Исполнение контракта (план) (формула) если есть way='п.4 ч.1 ст.93'"""
        from django.db.models import Q

        Services_way_ = await sync_to_async(list)(Services.objects.filter(
            Q(KOSGU=self.context_data['KOSGU']) & Q(DopFC=self.context_data['DopFC']) & Q(KTSSR=KTSSR) & Q(status=status) & Q(way='п.4 ч.1 ст.93')
        ))
        contract_price_sum_way = 0
        execution_contract_fact_sum_way = 0
        for service in Services_way_:
            contract_price_sum_way += await clean_number(service.contract_price if service.contract_price not in [None, 'None', ''] else 0)
            execution_contract_fact_sum_way += await clean_number(service.execution_contract_fact if service.execution_contract_fact not in [None, 'None', ''] else 0)

        return contract_price_sum_way, execution_contract_fact_sum_way

    async def Services_Two_save(self, Services_Two_):
        """Обновление второй базы"""

        Services_Two_.off_budget_planned = await self.calculate_contract_sums('2016100092', 'Запланировано')

        Services_Two_.budget_planned = await self.calculate_contract_sums('2016100000', 'Запланировано')

        Services_Two_.off_budget_bargaining = await self.calculate_contract_sums('2016100092', 'В торгах')

        Services_Two_.budget_bargaining = await self.calculate_contract_sums('2016100000', 'В торгах')

        Services_Two_.off_budget_concluded = await self.calculate_contract_sums('2016100092', 'Заключено')

        Services_Two_.budget_concluded = await self.calculate_contract_sums('2016100000', 'Заключено')

        Services_Two_.off_budget_completed = await self.calculate_contract_sums('2016100092', 'Исполнено')

        Services_Two_.budget_completed = await self.calculate_contract_sums('2016100000', 'Исполнено')

        Services_Two_.off_budget_execution = await self.calculate_contract_sums('2016100092', None)
        Services_Two_.budget_execution = await self.calculate_contract_sums('2016100000', None)

        await sync_to_async(Services_Two_.save)()

    async def process_update_user(self):
        Services_Two_ = await self.validate_Services_Two()

        await self.Services_Two_save(Services_Two_)

        Services_Two_ = await self.validate_Services_Two()

        await self.process_budget_services_two(Services_Two_)

        await self.message_service_update()

        # Кодируем query-параметры
        query_string = urlencode(self.context_data)

        # Формируем URL с query-параметрами
        redirect_url = f"{reverse('data_table_view')}?{query_string}"  # Замените 'index' на имя вашего URL-шаблона

        # Перенаправляем пользователя
        return HttpResponseRedirect(redirect_url)

        # Другие операции, такие как сохранение сервиса и т.д.

    async def process_update_user_two(self):
        from django.db.models import Q

        Services_Two_ = await self.validate_Services_Two()

        await self.process_budget_services_two(Services_Two_)

        await self.process_budget_services_three(None, Services_Two_)

        await self.message_service_update()

        # Кодируем query-параметры
        query_string = urlencode(self.context_data)

        # Формируем URL с query-параметрами
        redirect_url = f"{reverse('data_table_view')}?{query_string}"  # Замените 'index' на имя вашего URL-шаблона

        # Перенаправляем пользователя
        return HttpResponseRedirect(redirect_url)

        # Другие операции, такие как сохранение сервиса и т.д.

    async def process(self):
        """Предварительные вычислительные операции после обновления или добавления записи"""
        from django.db.models import Q

        Services_way_ = await sync_to_async(list)(Services.objects.filter(
            Q(KOSGU=self.context_data['KOSGU']) & Q(DopFC=self.context_data['DopFC']) & Q(KTSSR=self.context_data['KTSSR']) & Q(status=self.context_data['status']) & Q(way='п.4 ч.1 ст.93')
        ))
        contract_price_sum_way = 0
        execution_contract_fact_sum_way = 0
        for service in Services_way_:
            contract_price_sum_way += await clean_number(service.contract_price if service.contract_price not in [None, 'None', ''] else 0)
            execution_contract_fact_sum_way += await clean_number(service.execution_contract_fact if service.execution_contract_fact not in [None, 'None', ''] else 0)

        Services_Two_ = await self.validate_Services_Two()

        await self.Services_Two_save(Services_Two_)

        Services_Two_ = await self.validate_Services_Two()

        await self.process_budget_services_two(Services_Two_)

        await self.process_budget_services_three(contract_price_sum_way, Services_Two_)

    async def process_update(self):
        if not await self.validate_Services_Two():
            await self.validate_Services_Two_message()
            return render(self.request, 'edit.html', self.context_data)
        if not await self.validate_execution_plan():
            await self.validate_execution_plan_message()
            return render(self.request, 'edit.html', self.context_data)
        elif not await self.validate_execution_fact():
            await self.validate_execution_fact_message()
            return render(self.request, 'edit.html', self.context_data)

        execution_contract_plan = await self.calculate_execution_plan()
        execution_contract_fact = await self.calculate_execution_fact()
        saving = await clean_number(self.context_data['NMCC']) - await clean_number(self.context_data['contract_price'])

        if await clean_number(self.context_data['contract_price']) == 0:
            self.context_data['execution'] = 0  # Или любое другое значение по умолчанию, например `None` или сообщение об ошибке
        else:
            self.context_data['execution'] = round(await clean_number(execution_contract_fact) / await clean_number(self.context_data['contract_price']), 2) * 100

        self.context_data['contract_balance'] = await clean_number(self.context_data['contract_price']) - await clean_number(execution_contract_fact)

        await self.update_service(saving, execution_contract_plan, execution_contract_fact)

        await self.process()

        if not await self.total_costs(None):

            self.context_data['contract_price'] = '0'

            await self.update_service(saving, execution_contract_plan, execution_contract_fact)
            await self.process()

            await self.total_costs_message()
            return render(self.request, 'edit.html', self.context_data)

        await self.message_service_update()

        # Кодируем query-параметры
        query_string = urlencode(self.context_data)

        # Формируем URL с query-параметрами
        redirect_url = f"{reverse('data_table_view')}?{query_string}"  # Замените 'index' на имя вашего URL-шаблона

        # Перенаправляем пользователя
        return HttpResponseRedirect(redirect_url)

        # Другие операции, такие как сохранение сервиса и т.д.

    async def process_add(self):
        if not await self.validate_Services_Two():
            await self.validate_Services_Two_message()
            return render(self.request, 'add.html', self.context_data)
        elif not await self.validate_execution_plan():
            await self.validate_execution_plan_message()
            return render(self.request, 'add.html', self.context_data)
        elif not await self.validate_execution_fact():
            await self.validate_execution_fact_message()
            return render(self.request, 'add.html', self.context_data)

        execution_contract_plan = await self.calculate_execution_plan()
        execution_contract_fact = await self.calculate_execution_fact()
        saving = await clean_number(self.context_data['NMCC']) - await clean_number(self.context_data['contract_price'])

        if await clean_number(self.context_data['contract_price']) == 0:
            self.context_data['execution'] = 0  # Или любое другое значение по умолчанию, например `None` или сообщение об ошибке
        else:
            self.context_data['execution'] = round(await clean_number(execution_contract_fact) / await clean_number(self.context_data['contract_price']), 2) * 100

        self.context_data['contract_balance'] = await clean_number(self.context_data['contract_price']) - await clean_number(execution_contract_fact)

        new_service = Services()
        new_service = await self.creation_new_service(saving, execution_contract_plan, execution_contract_fact, new_service)

        Services_Two_ = await sync_to_async(lambda: Services_Two.objects.all())()

        await sync_to_async(new_service.save)()

        Services_Two_ = await self.validate_Services_Two()

        await self.Services_Two_save(Services_Two_)

        if not await self.total_costs(new_service):
            await self.total_costs_message()
            return render(self.request, 'add.html', self.context_data)

        await self.process()

        await self.message_service_add()

        # Кодируем query-параметры
        query_string = urlencode(self.context_data)

        # Формируем URL с query-параметрами
        redirect_url = f"{reverse('data_table_view')}?{query_string}"  # Замените 'index' на имя вашего URL-шаблона

        # Перенаправляем пользователя
        return HttpResponseRedirect(redirect_url)

        # Другие операции, такие как сохранение сервиса и т.д.

    async def process_delete(self, service):
        execution_contract_fact = await self.calculate_execution_fact()

        if await clean_number(self.context_data['contract_price']) == 0:
            self.context_data['execution'] = 0  # Или любое другое значение по умолчанию, например `None` или сообщение об ошибке
        else:
            self.context_data['execution'] = round(await clean_number(execution_contract_fact) / await clean_number(self.context_data['contract_price']), 2) * 100

        self.context_data['contract_balance'] = await clean_number(self.context_data['contract_price']) - await clean_number(execution_contract_fact)

        await self.process()

        await self.message_service_delete()

        # Кодируем query-параметры
        query_string = urlencode(self.context_data)

        # Формируем URL с query-параметрами
        redirect_url = f"{reverse('data_table_view')}?{query_string}"  # Замените 'index' на имя вашего URL-шаблона

        # Перенаправляем пользователя
        return HttpResponseRedirect(redirect_url)

        # Другие операции, такие как сохранение сервиса и т.д.

from urllib.parse import urlencode

@csrf_exempt  # Необходимо, если вы не используете CSRF-токены
async def update_record(request, row_id):
    if request.method == 'POST':
        try:
            # Возвращаем данные формы обратно в шаблон
            context_data = {
                'service': await sync_to_async(Services.objects.get)(id=row_id),
                'id_id': request.POST['id_id'],
                'name': request.POST['name'],
                'status': request.POST['status'],
                'way': request.POST['way'],
                'initiator': request.POST['initiator'],
                'KTSSR': request.POST['KTSSR'],
                'KOSGU': request.POST['KOSGU'],
                'DopFC': request.POST['DopFC'],
                'NMCC': request.POST['NMCC'],
                'counterparty': request.POST['counterparty'],
                'registration_number': request.POST['registration_number'],
                'contract_number': request.POST['contract_number'],
                'contract_date': request.POST['contract_date'],
                'end_date': request.POST['end_date'],
                'contract_price': request.POST['contract_price'],
                'january_one': request.POST['january_one'],
                'february': request.POST['february'],
                'march': request.POST['march'],
                'april': request.POST['april'],
                'may': request.POST['may'],
                'june': request.POST['june'],
                'july': request.POST['july'],
                'august': request.POST['august'],
                'september': request.POST['september'],
                'october': request.POST['october'],
                'november': request.POST['november'],
                'december': request.POST['december'],
                'january_two': request.POST['january_two'],
                'date_january_one': request.POST['date_january_one'],
                'sum_january_one': request.POST['sum_january_one'],
                'date_february': request.POST['date_february'],
                'sum_february': request.POST['sum_february'],
                'date_march': request.POST['date_march'],
                'sum_march':  request.POST['sum_march'],
                'date_april': request.POST['date_april'],
                'sum_april': request.POST['sum_april'],
                'date_may': request.POST['date_may'],
                'sum_may': request.POST['sum_may'],
                'date_june': request.POST['date_june'],
                'sum_june': request.POST['sum_june'],
                'date_july': request.POST['date_july'],
                'sum_july': request.POST['sum_july'],
                'date_august': request.POST['date_august'],
                'sum_august': request.POST['sum_august'],
                'date_september': request.POST['date_september'],
                'sum_september': request.POST['sum_september'],
                'date_october': request.POST['date_october'],
                'sum_october': request.POST['sum_october'],
                'date_november': request.POST['date_november'],
                'sum_november': request.POST['sum_november'],
                'date_december': request.POST['date_december'],
                'sum_december': request.POST['sum_december'],
                'date_january_two': request.POST['date_january_two'],
                'sum_january_two': request.POST['sum_january_two'],
                'execution': request.POST['execution'],
                'contract_balance': request.POST['contract_balance'],
                'execution_contract_fact': request.POST['execution_contract_fact'],
                'execution_contract_plan': request.POST['execution_contract_plan'],
                'saving': request.POST['saving'],
                'color': request.POST['color'],
                'row_id': row_id,
                'page': int(request.GET.get('page', '1')) if request.GET.get('page', '1').strip() else 1,
                'keyword_one': request.GET.get('keyword_one', None),
                'keyword_two': request.GET.get('keyword_two', None),
                'selected_column_one': request.GET.get('selected_column_one', None),
                'selected_column_two': request.GET.get('selected_column_two', None),
                'page_user': 1,
                'KOSGU_user': request.GET.get('KOSGU_user', None),
                'keyword_one_user': request.GET.get('keyword_one_user', None),
                'keyword_two_user': request.GET.get('keyword_two_user', None),
                'selected_column_one_user': request.GET.get('selected_column_one_user', None),
                'selected_column_two_user': request.GET.get('selected_column_two_user', None),
                'page_user_two': 1,
                'KOSGU_user_two': request.GET.get('KOSGU_user_two', None),
                'keyword_one_user_two': request.GET.get('keyword_one_user_two', None),
                'keyword_two_user_two': request.GET.get('keyword_two_user_two', None),
                'selected_column_one_user_two': request.GET.get('selected_column_one_user_two', None),
                'selected_column_two_user_two': request.GET.get('selected_column_two_user_two', None)
            }

            processor = ContractProcessor(context_data, request)
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
                'service_user': await sync_to_async(Services_Two.objects.get)(id=row_id),
                'id_id': request.POST['id_id'],
                'name': request.POST['name'],
                # 'status': request.POST['status'],
                # 'way': request.POST['way'],
                # 'initiator': request.POST['initiator'],
                # 'KTSSR': request.POST['KTSSR'],
                'KOSGU': request.POST['KOSGU'],
                'DopFC': request.POST['DopFC'],
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

                'budget_limit': request.POST['budget_limit'],
                'off_budget_limit': request.POST['off_budget_limit'],
                'budget_planned': request.POST['budget_planned'],
                'off_budget_planned': request.POST['off_budget_planned'],
                'budget_bargaining': request.POST['budget_bargaining'],
                'off_budget_bargaining': request.POST['off_budget_bargaining'],
                'budget_concluded': request.POST['budget_concluded'],
                'off_budget_concluded': request.POST['off_budget_concluded'],
                'budget_completed': request.POST['budget_completed'],
                'off_budget_completed': request.POST['off_budget_completed'],
                'budget_completed': request.POST['budget_completed'],
                'budget_execution': request.POST['budget_execution'],
                'off_budget_execution': request.POST['off_budget_execution'],
                'budget_remainder': request.POST['budget_remainder'],
                'off_budget_remainder': request.POST['off_budget_remainder'],
                'budget_plans': request.POST['budget_plans'],
                'off_budget_plans': request.POST['off_budget_plans'],

                'color': request.POST['color'],
                'row_id_user': row_id,
                'page': int(request.GET.get('page', '1')) if request.GET.get('page', '1').strip() else 1,
                'keyword_one': request.GET.get('keyword_one', None),
                'keyword_two': request.GET.get('keyword_two', None),
                'selected_column_one': request.GET.get('selected_column_one', None),
                'selected_column_two': request.GET.get('selected_column_two', None),
                'page_user': int(request.GET.get('page_user', '1')) if request.GET.get('page', '1').strip() else 1,
                'KOSGU_user': request.GET.get('KOSGU_user', None),
                'keyword_one_user': request.GET.get('keyword_one_user', None),
                'keyword_two_user': request.GET.get('keyword_two_user', None),
                'selected_column_one_user': request.GET.get('selected_column_one_user', None),
                'selected_column_two_user': request.GET.get('selected_column_two_user', None),
                'page_user_two': int(request.GET.get('page_user_two', '1')) if request.GET.get('page', '1').strip() else 1,
                'KOSGU_user_two': request.GET.get('KOSGU_user_two', None),
                'keyword_one_user_two': request.GET.get('keyword_one_user_two', None),
                'keyword_two_user_two': request.GET.get('keyword_two_user_two', None),
                'selected_column_one_user_two': request.GET.get('selected_column_one_user_two', None),
                'selected_column_two_user_two': request.GET.get('selected_column_two_user_two', None)
            }

            context_data['service_user'].id_id = context_data['id_id']
            context_data['service_user'].name = context_data['name']
            context_data['service_user'].KOSGU = context_data['KOSGU']
            context_data['service_user'].DopFC = context_data['DopFC']
            context_data['service_user'].budget_limit = context_data['budget_limit']
            context_data['service_user'].off_budget_limit = context_data['off_budget_limit']
            context_data['service_user'].budget_planned = context_data['budget_planned']
            context_data['service_user'].off_budget_planned = context_data['off_budget_planned']
            context_data['service_user'].budget_bargaining = context_data['budget_bargaining']
            context_data['service_user'].off_budget_bargaining = context_data['off_budget_bargaining']
            context_data['service_user'].budget_concluded = context_data['budget_concluded']
            context_data['service_user'].off_budget_concluded = context_data['off_budget_concluded']
            context_data['service_user'].budget_completed = context_data['budget_completed']
            context_data['service_user'].off_budget_completed = context_data['off_budget_completed']
            context_data['service_user'].budget_execution = context_data['budget_execution']
            context_data['service_user'].off_budget_execution = context_data['off_budget_execution']
            context_data['service_user'].budget_remainder = context_data['budget_remainder']
            context_data['service_user'].off_budget_remainder = context_data['off_budget_remainder']
            context_data['service_user'].budget_plans = context_data['budget_plans']
            context_data['service_user'].off_budget_plans = context_data['off_budget_plans']
            context_data['service_user'].color = context_data['color']

            await sync_to_async(context_data['service_user'].save)()

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
                'service_user_two': await sync_to_async(Services_Three.objects.get)(id=row_id),
                'id_id': request.POST['id_id'],
                # 'name': request.POST['name'],
                # 'status': request.POST['status'],
                # 'way': request.POST['way'],
                # 'initiator': request.POST['initiator'],
                # 'KTSSR': request.POST['KTSSR'],
                'KOSGU': request.POST['KOSGU'],
                'DopFC': request.POST['DopFC'],
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

                # 'budget_limit': request.POST['budget_limit'],
                # 'off_budget_limit': request.POST['off_budget_limit'],
                'budget_planned': request.POST['budget_planned'],
                'off_budget_planned': request.POST['off_budget_planned'],
                # 'budget_bargaining': request.POST['budget_bargaining'],
                # 'off_budget_bargaining': request.POST['off_budget_bargaining'],
                'budget_concluded': request.POST['budget_concluded'],
                'off_budget_concluded': request.POST['off_budget_concluded'],
                # 'budget_completed': request.POST['budget_completed'],
                # 'off_budget_completed': request.POST['off_budget_completed'],
                # 'budget_completed': request.POST['budget_completed'],
                # 'budget_execution': request.POST['budget_execution'],
                # 'off_budget_execution': request.POST['off_budget_execution'],
                'budget_remainder': request.POST['budget_remainder'],
                'off_budget_remainder': request.POST['off_budget_remainder'],
                # 'budget_plans': request.POST['budget_plans'],
                # 'off_budget_plans': request.POST['off_budget_plans'],

                'color': request.POST['color'],
                'row_id_user_two': row_id,
                'page': int(request.GET.get('page', '1')) if request.GET.get('page', '1').strip() else 1,
                'keyword_one': request.GET.get('keyword_one', None),
                'keyword_two': request.GET.get('keyword_two', None),
                'selected_column_one': request.GET.get('selected_column_one', None),
                'selected_column_two': request.GET.get('selected_column_two', None),
                'page_user': int(request.GET.get('page_user', '1')) if request.GET.get('page', '1').strip() else 1,
                'KOSGU_user': request.GET.get('KOSGU_user', None),
                'keyword_one_user': request.GET.get('keyword_one_user', None),
                'keyword_two_user': request.GET.get('keyword_two_user', None),
                'selected_column_one_user': request.GET.get('selected_column_one_user', None),
                'selected_column_two_user': request.GET.get('selected_column_two_user', None),
                'page_user_two': int(request.GET.get('page_user_two', '1')) if request.GET.get('page', '1').strip() else 1,
                'KOSGU_user_two': request.GET.get('KOSGU_user_two', None),
                'keyword_one_user_two': request.GET.get('keyword_one_user_two', None),
                'keyword_two_user_two': request.GET.get('keyword_two_user_two', None),
                'selected_column_one_user_two': request.GET.get('selected_column_one_user_two', None),
                'selected_column_two_user_two': request.GET.get('selected_column_two_user_two', None)
            }

            context_data['service_user_two'].id_id = context_data['id_id']
            # context_data['service_user'].name = context_data['name']
            context_data['service_user_two'].KOSGU = context_data['KOSGU']
            context_data['service_user_two'].DopFC = context_data['DopFC']
            # context_data['service_user'].budget_limit = context_data['budget_limit']
            # context_data['service_user'].off_budget_limit = context_data['off_budget_limit']
            context_data['service_user_two'].budget_planned = context_data['budget_planned']
            context_data['service_user_two'].off_budget_planned = context_data['off_budget_planned']
            # context_data['service_user'].budget_bargaining = context_data['budget_bargaining']
            # context_data['service_user'].off_budget_bargaining = context_data['off_budget_bargaining']
            context_data['service_user_two'].budget_concluded = context_data['budget_concluded']
            context_data['service_user_two'].off_budget_concluded = context_data['off_budget_concluded']
            # context_data['service_user'].budget_completed = context_data['budget_completed']
            # context_data['service_user'].off_budget_completed = context_data['off_budget_completed']
            # context_data['service_user'].budget_execution = context_data['budget_execution']
            # context_data['service_user'].off_budget_execution = context_data['off_budget_execution']
            context_data['service_user_two'].budget_remainder = context_data['budget_remainder']
            context_data['service_user_two'].off_budget_remainder = context_data['off_budget_remainder']
            # context_data['service_user'].budget_plans = context_data['budget_plans']
            # context_data['service_user'].off_budget_plans = context_data['off_budget_plans']
            context_data['service_user_two'].color = context_data['color']

            await sync_to_async(context_data['service_user_two'].save)()

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
                # 'service': await sync_to_async(Services.objects.get)(id=row_id),
                # 'id_id': request.POST['id_id'],
                'name': request.POST['name'],
                'status': request.POST['status'],
                'way': request.POST['way'],
                'initiator': request.POST['initiator'],
                'KTSSR': request.POST['KTSSR'],
                'KOSGU': request.POST['KOSGU'],
                'DopFC': request.POST['DopFC'],
                'NMCC': request.POST['NMCC'],
                'counterparty': request.POST['counterparty'],
                'registration_number': request.POST['registration_number'],
                'contract_number': request.POST['contract_number'],
                'contract_date': request.POST['contract_date'],
                'end_date': request.POST['end_date'],
                'contract_price': request.POST['contract_price'],
                'january_one': request.POST['january_one'],
                'february': request.POST['february'],
                'march': request.POST['march'],
                'april': request.POST['april'],
                'may': request.POST['may'],
                'june': request.POST['june'],
                'july': request.POST['july'],
                'august': request.POST['august'],
                'september': request.POST['september'],
                'october': request.POST['october'],
                'november': request.POST['november'],
                'december': request.POST['december'],
                'january_two': request.POST['january_two'],
                'date_january_one': request.POST['date_january_one'],
                'sum_january_one': request.POST['sum_january_one'],
                'date_february': request.POST['date_february'],
                'sum_february': request.POST['sum_february'],
                'date_march': request.POST['date_march'],
                'sum_march':  request.POST['sum_march'],
                'date_april': request.POST['date_april'],
                'sum_april': request.POST['sum_april'],
                'date_may': request.POST['date_may'],
                'sum_may': request.POST['sum_may'],
                'date_june': request.POST['date_june'],
                'sum_june': request.POST['sum_june'],
                'date_july': request.POST['date_july'],
                'sum_july': request.POST['sum_july'],
                'date_august': request.POST['date_august'],
                'sum_august': request.POST['sum_august'],
                'date_september': request.POST['date_september'],
                'sum_september': request.POST['sum_september'],
                'date_october': request.POST['date_october'],
                'sum_october': request.POST['sum_october'],
                'date_november': request.POST['date_november'],
                'sum_november': request.POST['sum_november'],
                'date_december': request.POST['date_december'],
                'sum_december': request.POST['sum_december'],
                'date_january_two': request.POST['date_january_two'],
                'sum_january_two': request.POST['sum_january_two'],
                'execution': request.POST['execution'],
                'contract_balance': request.POST['contract_balance'],
                'execution_contract_fact': request.POST['execution_contract_fact'],
                'execution_contract_plan': request.POST['execution_contract_plan'],
                'saving': request.POST['saving'],
                'color': request.POST['color'],
                # 'row_id': row_id,
                'page': int(request.GET.get('page', '1')) if request.GET.get('page', '1').strip() else 1,
                'keyword_one': request.GET.get('keyword_one', None),
                'keyword_two': request.GET.get('keyword_two', None),
                'selected_column_one': request.GET.get('selected_column_one', None),
                'selected_column_two': request.GET.get('selected_column_two', None),
                'page_user': 1,
                'KOSGU_user': request.GET.get('KOSGU_user', None),
                'keyword_one_user': request.GET.get('keyword_one_user', None),
                'keyword_two_user': request.GET.get('keyword_two_user', None),
                'selected_column_one_user': request.GET.get('selected_column_one_user', None),
                'selected_column_two_user': request.GET.get('selected_column_two_user', None),
                'page_user_two': 1,
                'KOSGU_user_two': request.GET.get('KOSGU_user_two', None),
                'keyword_one_user_two': request.GET.get('keyword_one_user_two', None),
                'keyword_two_user_two': request.GET.get('keyword_two_user_two', None),
                'selected_column_one_user_two': request.GET.get('selected_column_one_user_two', None),
                'selected_column_two_user_two': request.GET.get('selected_column_two_user_two', None)
            }

            processor = ContractProcessor(context_data, request)
            return await processor.process_add()
        except Services.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Service not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON.'}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)

@csrf_exempt  # Необходимо, если вы не используете CSRF-токены
async def delete_record(request, row_id):
    if request.method == 'POST':
        try:

            # Найдите запись по ID и обновите цвет
            service = await sync_to_async(Services.objects.get)(id=row_id)

            # Возвращаем данные формы обратно в шаблон
            context_data = {
                # 'service': await sync_to_async(Services.objects.get)(id=row_id),
                'id_id': service.id_id,
                'name': service.name,
                'status': service.status,
                'way': service.way,
                'initiator': service.initiator,
                'KTSSR': service.KTSSR,
                'KOSGU': service.KOSGU,
                'DopFC': service.DopFC,
                'NMCC': service.NMCC,
                'counterparty': service.counterparty,
                'registration_number': service.registration_number,
                'contract_number': service.contract_number,
                'contract_date': service.contract_date,
                'end_date': service.end_date,
                'contract_price': service.contract_price,
                'january_one': service.january_one,
                'february': service.february,
                'march': service.march,
                'april': service.april,
                'may': service.may,
                'june': service.june,
                'july': service.july,
                'august': service.august,
                'september': service.september,
                'october': service.october,
                'november': service.november,
                'december': service.december,
                'january_two': service.january_two,
                'date_january_one': service.date_january_one,
                'sum_january_one': service.sum_january_one,
                'date_february': service.date_february,
                'sum_february': service.sum_february,
                'date_march': service.date_march,
                'sum_march':  service.sum_march,
                'date_april': service.date_april,
                'sum_april': service.sum_april,
                'date_may': service.date_may,
                'sum_may': service.sum_may,
                'date_june': service.date_june,
                'sum_june': service.sum_june,
                'date_july': service.date_july,
                'sum_july': service.sum_july,
                'date_august': service.date_august,
                'sum_august': service.sum_august,
                'date_september': service.date_september,
                'sum_september': service.sum_september,
                'date_october': service.date_october,
                'sum_october': service.sum_october,
                'date_november': service.date_november,
                'sum_november': service.sum_november,
                'date_december': service.date_december,
                'sum_december': service.sum_december,
                'date_january_two': service.date_january_two,
                'sum_january_two': service.sum_january_two,
                'execution': service.execution,
                'contract_balance': service.contract_balance,
                'execution_contract_fact': service.execution_contract_fact,
                'execution_contract_plan': service.execution_contract_plan,
                'saving': service.saving,
                'color': service.color,
                # 'row_id': row_id,
                # 'page': int(request.GET.get('page', 1)),
                # 'keyword_one': request.GET.get('keyword_one', None),
                # 'keyword_two': request.GET.get('keyword_two', None),
                # 'selected_column_one': request.GET.get('selected_column_one', None),
                # 'selected_column_two': request.GET.get('selected_column_two', None),
                # 'page_user': 1,
                # 'KOSGU_user': request.GET.get('KOSGU_user', None),
                # 'keyword_one_user': request.GET.get('keyword_one_user', None),
                # 'keyword_two_user': request.GET.get('keyword_two_user', None),
                # 'selected_column_one_user': request.GET.get('selected_column_one_user', None),
                # 'selected_column_two_user': request.GET.get('selected_column_two_user', None),
                # 'page_user_two': 1,
                # 'KOSGU_user_two': request.GET.get('KOSGU_user_two', None),
                # 'keyword_one_user_two': request.GET.get('keyword_one_user_two', None),
                # 'keyword_two_user_two': request.GET.get('keyword_two_user_two', None),
                # 'selected_column_one_user_two': request.GET.get('selected_column_one_user_two', None),
                # 'selected_column_two_user_two': request.GET.get('selected_column_two_user_two', None)
            }

            processor = ContractProcessor(context_data, request)
            return await processor.process_delete(service)
        except Services.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Service not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON.'}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)

from .models import UploadedFile
import pandas as pd

@csrf_exempt  # Если используете fetch, нужно отключить CSRF или передавать токен
async def upload_file(request):
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

                    from django.db import connection

                    if data_to_insert:
                        # Вставьте данные в базу данных
                        with connection.cursor() as cursor:
                            cursor.execute(insert_query, data_to_insert)  # Передаем данные как кортеж
                        # cursor.executemany(insert_query, data_to_insert)
                        # conn.commit()
                        return JsonResponse({"message": f"Данные из файла {uploaded_file.name} успешно загружены!", "status": "success"})
                    else:
                        return JsonResponse({"message": f"Ошибка при обработке файла: Данные не загружены", "status": "error"}, status=400)

                    # # Сохранение файла в папку file/
                    # file_instance = UploadedFile(file=uploaded_file)
                    # file_instance.save()
                else:
                    return JsonResponse({"message": "Нет соответствия количества столбцов", "status": "error"}, status=400)

            except Exception as e:
                return JsonResponse({"message": f"Ошибка при обработке файла: {str(e)}", "status": "error"}, status=400)
        else:
            return JsonResponse({"message": "Только файлы .xlsx разрешены", "status": "error"}, status=400)

    return JsonResponse({"message": "Ошибка загрузки файла"}, status=400)