from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Services, ServicesVault, ServicesTwo
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator
from django.shortcuts import render
import re
from django.db.models import Sum
from asgiref.sync import sync_to_async

import asyncio

async def skeleton(request, user, contract_date, end_date, keyword_one, keyword_two, selected_column_one, selected_column_two, page, KOSGU_user, keyword_one_user, keyword_two_user, selected_column_one_user, selected_column_two_user, page_user, KOSGU_user_two, keyword_one_user_two, keyword_two_user_two, selected_column_one_user_two, selected_column_two_user_two, page_user_two):
    contract_date = None if contract_date == 'None' else contract_date
    end_date = None if end_date == 'None' else end_date
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

    # Регулярные выражения для форматов дат
    pattern_dd_mm_yyyy = r'\b\d{2}\.\d{2}\.\d{4}\b'
    pattern_yyyy_mm_dd = r'\b\d{4}-\d{2}-\d{2}\b'

    # Получаем все уникальные значения year и date_number_no_one
    all_years = await sync_to_async(lambda: list(Services.objects.values('contract_date').distinct()))()
    all_end_date = await sync_to_async(lambda: list(Services.objects.values('end_date').distinct()))()
    all_KOSGU_user = await sync_to_async(lambda: list(ServicesVault.objects.values('KOSGU').distinct()))()
    all_KOSGU_user_two = await sync_to_async(lambda: list(ServicesTwo.objects.values('KOSGU').distinct()))()

    async def process_service_data(all_data, field_name):
        service_data = set()
        empty_found = False

        for item in all_data:
            field_value = item.get(field_name, None)
            if not field_value:
                empty_found = True
                continue

            matches_dd_mm_yyyy = re.findall(pattern_dd_mm_yyyy, field_value)
            matches_yyyy_mm_dd = re.findall(pattern_yyyy_mm_dd, field_value)

            service_data.update([date_str[-4:] for date_str in matches_dd_mm_yyyy])
            service_data.update([date_str[:4] for date_str in matches_yyyy_mm_dd])

        service_data = sorted({str(int(year)) for year in service_data if year.isdigit()})
        if empty_found:
            service_data.insert(0, None)
        return service_data

    service_years = await process_service_data(all_years, 'contract_date')
    service_end_date = await process_service_data(all_end_date, 'end_date')
    service_KOSGU_user = await process_service_data(all_KOSGU_user, 'KOSGU')
    service_KOSGU_user_two = await process_service_data(all_KOSGU_user_two, 'KOSGU')

    # Построение запроса
    query = await sync_to_async(lambda: Services.objects.all())()
    query_user = await sync_to_async(lambda: ServicesVault.objects.all())()
    query_user_two = await sync_to_async(lambda: ServicesTwo.objects.all())()

    if contract_date == 'No':
        contract_date = None
    if end_date == 'No':
        end_date = None

    async def apply_filters(query, filters):
        for filter_func in filters:
            query = await sync_to_async(filter_func)(query)
        return query

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
    query_user = await apply_keyword_filter(query_user, keyword_one_user, selected_column_one_user, ServicesVault)
    query_user = await apply_keyword_filter(query_user, keyword_two_user, selected_column_two_user, ServicesVault)
    query_user_two = await apply_keyword_filter(query_user_two, keyword_one_user_two, selected_column_one_user_two, ServicesTwo)
    query_user_two = await apply_keyword_filter(query_user_two, keyword_two_user_two, selected_column_two_user_two, ServicesTwo)

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

        query_user = await sync_to_async(lambda: ServicesVault.objects.all())()

        total_services_full_user = await sync_to_async(lambda: query_user.count())()
        page_user = (total_services_full_user + per_page - 1) // per_page
    else:
        page_user = int(request.GET.get('page_user', 1))

    total_pages_full_user_two = request.GET.get('total_pages_full_user_two', None)

    if total_pages_full_user_two:
        per_page = 20

        query_user_two = await sync_to_async(lambda: ServicesTwo.objects.all())()

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
            service = await sync_to_async(ServicesVault.objects.get)(id=row_id)
            service.color = color
            await sync_to_async(service.save)()

            return JsonResponse({'success': True, 'id': service.id, 'color': service.color})
        except ServicesVault.DoesNotExist:
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
            service = await sync_to_async(ServicesTwo.objects.get)(id=row_id)
            service.color = color
            await sync_to_async(service.save)()

            return JsonResponse({'success': True, 'id': service.id, 'color': service.color})
        except ServicesVault.DoesNotExist:
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

@csrf_exempt  # Необходимо, если вы не используете CSRF-токены
async def edit(request, row_id):
    page = int(request.GET.get('page', 1))
    keyword_one = request.GET.get('keyword_one', None)
    keyword_two = request.GET.get('keyword_two', None)
    selected_column_one = request.GET.get('selected_column_one', None)
    selected_column_two = request.GET.get('selected_column_two', None)
    selected_contract_date = request.GET.get('contract_date', "No")
    selected_end_date = request.GET.get('end_date', "No")

    user = request.user

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
        'user': user,
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

@csrf_exempt  # Необходимо, если вы не используете CSRF-токены
async def edit_user(request, row_id):
    page_user = int(request.GET.get('page_user', 1))
    keyword_one_user = request.GET.get('keyword_one_user', None)
    keyword_two_user = request.GET.get('keyword_two_user', None)
    selected_column_one_user = request.GET.get('selected_column_one_user', None)
    selected_column_two_user = request.GET.get('selected_column_two_user', None)
    selected_contract_date_user = request.GET.get('selected_contract_date_user', "No")
    selected_end_date_user = request.GET.get('selected_end_date_user', "No")

    user = request.user

    # Получаем объект service_user по id
    service_user = await sync_to_async(ServicesVault.objects.get)(id=row_id)

    # Подготовка контекста для шаблона
    context = {
        'service_user': service_user,
        'user': user,
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

@csrf_exempt  # Необходимо, если вы не используете CSRF-токены
async def edit_user_two(request, row_id):
    page_user = int(request.GET.get('page_user', 1))
    keyword_one_user = request.GET.get('keyword_one_user', None)
    keyword_two_user = request.GET.get('keyword_two_user', None)
    selected_column_one_user = request.GET.get('selected_column_one_user', None)
    selected_column_two_user = request.GET.get('selected_column_two_user', None)
    selected_contract_date_user = request.GET.get('selected_contract_date_user', "No")
    selected_end_date_user = request.GET.get('selected_end_date_user', "No")

    user = request.user

    # Получаем объект service_user_two по id
    service_user_two = await sync_to_async(ServicesTwo.objects.get)(id=row_id)

    # Подготовка контекста для шаблона
    context = {
        'service_user_two': service_user_two,
        'user': user,
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

async def clean_number(value):
    if isinstance(value, (int, float)):
        return float(value)  # Уже число, возвращаем как есть
    if not value or value.strip() == '':
        return 0.0  # Пустая строка обрабатывается как 0.0
    return float(value.replace(' ', '').replace(',', '.'))

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
                # await sync_to_async(messages.error)(self.request, 'Значение поля «Исполнение контракта (план) должно равняться полю «Цена контракта»')
                return False
        return True

    async def validate_execution_plan_message(self):
        await sync_to_async(messages.error)(self.request, 'Значение поля «Исполнение контракта (план) должно равняться полю «Цена контракта»')

    async def validate_execution_fact(self):
        execution_contract_plan = await self.calculate_execution_plan()
        execution_contract_fact = await self.calculate_execution_fact()
        if execution_contract_plan != execution_contract_fact and self.context_data['status'] == 'Исполнено':
            # await sync_to_async(messages.error)(self.request, 'Нельзя выставить статус "Исполнено" при неравенстве ячеек «Исполнение контракта (факт)» и «Исполнение контракта (план)»')
            return False
        return True

    async def validate_execution_fact_message(self):
        await sync_to_async(messages.error)(self.request, 'Нельзя выставить статус "Исполнено" при неравенстве ячеек «Исполнение контракта (факт)» и «Исполнение контракта (план)»')

    async def validate_ServicesVault(self):
        try:
            from django.db.models import Q

            ServicesVault_ = await sync_to_async(ServicesVault.objects.get)(
                Q(KOSGU=self.context_data['KOSGU']) & Q(DopFC=self.context_data['DopFC'])
            )
            return ServicesVault_
        except:
            # await sync_to_async(messages.error)(self.request, 'Нет сопоставления КОСГУ с ДопФК')
            return False

    async def validate_ServicesVault_message(self):
        await sync_to_async(messages.error)(self.request, 'Нет сопоставления КОСГУ с ДопФК')

    async def validate_Services(self):
        from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

        try:
            Services_ = await sync_to_async(Services.objects.get)(name=self.context_data['name'])
            # await sync_to_async(messages.error)(self.request, 'Вы добавляете дубликат в Наименовании')

            print('validate_Services_1')

            return False
        except MultipleObjectsReturned:
            Services_ = await sync_to_async(lambda: Services.objects.filter(name=self.context_data['name']).first())()
            # await sync_to_async(messages.error)(self.request, 'Вы добавляете дубликат в Наименовании')

            print('validate_Services_2')

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
        service = self.context_data['service']
        for key, value in self.context_data.items():
            if key == saving:
                setattr(service, key, saving)
            elif key == execution_contract_plan:
                setattr(service, key, execution_contract_plan)
            elif key == execution_contract_fact:
                setattr(service, key, execution_contract_fact)
            else:
                setattr(service, key, value)
        await sync_to_async(service.save)()

    async def save_service(self, saving, execution_contract_plan, execution_contract_fact, new_service):
        # Получаем следующий ID
        from django.db import connection

        def get_latest_service():
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id_id FROM services_base
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

        await sync_to_async(new_service.save)()

    async def calculate_contract_sums(self, KTSSR, status):
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

    async def process_budget(self, ServicesVault_):
        # Создаем список месяцев
        budget = [
            ServicesVault_.budget_limit if ServicesVault_.budget_limit not in [None, 'None', ''] else 0,
            ServicesVault_.budget_bargaining if ServicesVault_.budget_bargaining not in [None, 'None', ''] else 0,
            ServicesVault_.budget_concluded if ServicesVault_.budget_concluded not in [None, 'None', ''] else 0,
            ServicesVault_.budget_completed if ServicesVault_.budget_completed not in [None, 'None', ''] else 0
        ]

        # Асинхронно обрабатываем все месяцы
        cleaned_numbers = await asyncio.gather(*(clean_number(number) for number in budget))

        # Суммируем результат
        ServicesVault_.budget_remainder = cleaned_numbers[0] - sum(cleaned_numbers[1:])

        # Создаем список месяцев
        off_budget = [
            ServicesVault_.off_budget_limit if ServicesVault_.off_budget_limit not in [None, 'None', ''] else 0,
            ServicesVault_.off_budget_bargaining if ServicesVault_.off_budget_bargaining not in [None, 'None', ''] else 0,
            ServicesVault_.off_budget_concluded if ServicesVault_.off_budget_concluded not in [None, 'None', ''] else 0,
            ServicesVault_.off_budget_completed if ServicesVault_.off_budget_completed not in [None, 'None', ''] else 0
        ]

        # Асинхронно обрабатываем все месяцы
        cleaned_numbers = await asyncio.gather(*(clean_number(number) for number in off_budget))

        # Суммируем результат
        ServicesVault_.off_budget_remainder = cleaned_numbers[0] - sum(cleaned_numbers[1:])

        # Расчет планов
        ServicesVault_.budget_plans = await self.clean_number_two(ServicesVault_.budget_remainder) - await self.clean_number_two(ServicesVault_.budget_planned)
        ServicesVault_.off_budget_plans = await self.clean_number_two(ServicesVault_.off_budget_remainder) - await self.clean_number_two(ServicesVault_.off_budget_planned)

        if any(x < 0 for x in [await clean_number(ServicesVault_.budget_remainder),
                            await clean_number(ServicesVault_.off_budget_remainder),
                            await clean_number(ServicesVault_.budget_plans),
                            await clean_number(ServicesVault_.off_budget_plans)]):
            ServicesVault_.color = '#ffebeb'
        else:
            ServicesVault_.color = ''

        await sync_to_async(ServicesVault_.save)()

    async def process_services_two(self, contract_price_sum_way, ServicesVault_, ServicesTwo_):
        try:
            if self.context_data['status']:

                from django.db.models import Q

                if self.context_data['status'] == 'Заключено' and self.context_data['KTSSR'] == '2016100092':
                    ServicesTwo_.off_budget_concluded = contract_price_sum_way if contract_price_sum_way else ServicesTwo_.off_budget_concluded
                    ServicesTwo_.off_budget_remainder = await clean_number(ServicesTwo_.off_budget_planned) - await clean_number(contract_price_sum_way)
                elif self.context_data['status'] == 'Заключено' and self.context_data['KTSSR'] == '2016100000':
                    ServicesTwo_.budget_concluded = contract_price_sum_way if contract_price_sum_way else ServicesTwo_.budget_concluded
                    ServicesTwo_.budget_remainder = await clean_number(ServicesTwo_.budget_planned) - await clean_number(contract_price_sum_way)

            if any(x < 0 for x in [await clean_number(ServicesVault_.budget_remainder),
                                await clean_number(ServicesVault_.off_budget_remainder),
                                await clean_number(ServicesVault_.budget_plans),
                                await clean_number(ServicesVault_.off_budget_plans)]):
                ServicesTwo_.color = '#ffebeb'
            else:
                ServicesTwo_.color = ''

            await sync_to_async(ServicesTwo_.save)()

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

    async def aggregate_fields(self, query_user, fields):
        results = {}
        for field in fields:
            # Асинхронно выполняем агрегацию по каждому полю
            result = await sync_to_async(lambda: query_user.aggregate(**{f'{field}__sum': Sum(field)}))()
            # Получаем значение суммы или 0, если оно None
            results[field] = result[f'{field}__sum'] or 0
        return results

    async def total_costs(self, query_user, new_service):
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
        aggregated_results = await self.aggregate_fields(query_user, fields)

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
            await sync_to_async(new_service.delete)()
            # await sync_to_async(messages.error)(self.request, 'Запрещено вносить новую строку, если после ее ввода сумма контактов по соответствующему КЦСР, КОСГУ и ДопФК превысит значение поля «Лимиты»')

            return False
            # return render(self.request, 'add.html', self.context_data)

        if total_costs_calc['total_cost_2'] < (total_costs_calc['total_cost_4'] or total_costs_calc['total_cost_5'] or total_costs_calc['total_cost_8'] or total_costs_calc['total_cost_10']):
            await sync_to_async(new_service.delete)()
            # await sync_to_async(messages.error)(self.request, 'Запрещено вносить новую строку, если после ее ввода сумма контактов по соответствующему КЦСР, КОСГУ и ДопФК превысит значение поля «Лимиты»')

            return False
            # return render(self.request, 'add.html', self.context_data)
        return True

    async def total_costs_message(self):
        await sync_to_async(messages.error)(self.request, 'Запрещено вносить новую строку, если после ее ввода сумма контактов по соответствующему КЦСР, КОСГУ и ДопФК превысит значение поля «Лимиты»')

    async def process_update_user(self):
        from django.db.models import Q

        # ServicesVault_ = await sync_to_async(ServicesVault.objects.get)(
        #     Q(KOSGU=self.context_data['KOSGU']) & Q(DopFC=self.context_data['DopFC'])
        # )

        ServicesTwo_ = await sync_to_async(ServicesTwo.objects.get)(
            Q(KOSGU=self.context_data['KOSGU']) & Q(DopFC=self.context_data['DopFC'])
        )

        await self.process_services_two(None, None, ServicesTwo_)

        await self.message_service_update()

        # redirect(f"/?{urlencode(self.context_data)}")

        # Кодируем query-параметры
        query_string = urlencode(self.context_data)

        # Формируем URL с query-параметрами
        redirect_url = f"{reverse('data_table_view')}?{query_string}"  # Замените 'index' на имя вашего URL-шаблона

        # Перенаправляем пользователя
        return HttpResponseRedirect(redirect_url)

        # Другие операции, такие как сохранение сервиса и т.д.

    async def process_update(self):
        # print('ПОПАЛ_FF')
        # if not await self.validate_Services():
        #     print('ПОПАЛ_11')
        #     await self.validate_Services_message()

        #     return render(self.request, 'edit.html', self.context_data)
        #     # return
        if not await self.validate_ServicesVault():
            print('ПОПАЛ_22')
            await self.validate_ServicesVault_message()

            return render(self.request, 'edit.html', self.context_data)
        if not await self.validate_execution_plan():
            print('ПОПАЛ_33')
            await self.validate_execution_plan_message()

            # # Кодируем query-параметры
            # query_string = urlencode(self.context_data)

            # # Формируем URL с query-параметрами
            # redirect_url = f"{reverse('edit', args=[self.context_data['row_id']])}?{query_string}"  # Замените 'index' на имя вашего URL-шаблона

            # # Перенаправляем пользователя
            # return HttpResponseRedirect(redirect_url)

            return render(self.request, 'edit.html', self.context_data)
        elif not await self.validate_execution_fact():
            print('ПОПАЛ_44')
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

        from django.db.models import Q

        Services_way_ = await sync_to_async(list)(Services.objects.filter(
            Q(KOSGU=self.context_data['KOSGU']) & Q(DopFC=self.context_data['DopFC']) & Q(KTSSR=self.context_data['KTSSR']) & Q(status=self.context_data['status']) & Q(way='п.4 ч.1 ст.93')
        ))
        contract_price_sum_way = 0
        execution_contract_fact_sum_way = 0
        for service in Services_way_:
            contract_price_sum_way += await clean_number(service.contract_price if service.contract_price not in [None, 'None', ''] else 0)
            execution_contract_fact_sum_way += await clean_number(service.execution_contract_fact if service.execution_contract_fact not in [None, 'None', ''] else 0)

        ServicesVault_ = await self.validate_ServicesVault()

        ServicesVault_.off_budget_planned = await self.calculate_contract_sums('2016100092', 'Запланировано')

        ServicesVault_.budget_planned = await self.calculate_contract_sums('2016100000', 'Запланировано')

        ServicesVault_.off_budget_bargaining = await self.calculate_contract_sums('2016100092', 'В торгах')

        ServicesVault_.budget_bargaining = await self.calculate_contract_sums('2016100000', 'В торгах')

        ServicesVault_.off_budget_concluded = await self.calculate_contract_sums('2016100092', 'Заключено')

        ServicesVault_.budget_concluded = await self.calculate_contract_sums('2016100000', 'Заключено')

        ServicesVault_.off_budget_completed = await self.calculate_contract_sums('2016100092', 'Исполнено')

        ServicesVault_.budget_completed = await self.calculate_contract_sums('2016100000', 'Исполнено')

        if self.context_data['KTSSR'] == '2016100092':
            ServicesVault_.off_budget_execution = await self.calculate_contract_sums('2016100092', None)
        elif self.context_data['KTSSR'] == '2016100000':
            ServicesVault_.budget_execution = await self.calculate_contract_sums('2016100000', None)

        await sync_to_async(ServicesVault_.save)()

        ServicesVault_ = await self.validate_ServicesVault()

        await self.process_budget(ServicesVault_)

        # ServicesVault_ = await sync_to_async(ServicesVault.objects.get)(
        #     Q(KOSGU=self.context_data['KOSGU']) & Q(DopFC=self.context_data['DopFC'])
        # )

        ServicesTwo_ = await sync_to_async(ServicesTwo.objects.get)(
            Q(KOSGU=self.context_data['KOSGU']) & Q(DopFC=self.context_data['DopFC'])
        )

        print(ServicesVault_)

        await self.process_services_two(contract_price_sum_way, ServicesVault_, ServicesTwo_)

        await self.message_service_update()

        print('ПОПАЛ_6')

        # redirect(f"/?{urlencode(self.context_data)}")

        # Кодируем query-параметры
        query_string = urlencode(self.context_data)

        # Формируем URL с query-параметрами
        redirect_url = f"{reverse('data_table_view')}?{query_string}"  # Замените 'index' на имя вашего URL-шаблона

        # Перенаправляем пользователя
        return HttpResponseRedirect(redirect_url)

        # Другие операции, такие как сохранение сервиса и т.д.

    async def process_add(self):
        if not await self.validate_Services():
            print('ПОПАЛ_11')
            await self.validate_Services_message()

            return render(self.request, 'add.html', self.context_data)
        elif not await self.validate_ServicesVault():
            print('ПОПАЛ_22')
            await self.validate_ServicesVault_message()

            return render(self.request, 'add.html', self.context_data)
        if not await self.validate_execution_plan():
            print('ПОПАЛ_33')
            await self.validate_execution_plan_message()

            # # Кодируем query-параметры
            # query_string = urlencode(self.context_data)

            # # Формируем URL с query-параметрами
            # redirect_url = f"{reverse('add')}?{query_string}"  # Замените 'index' на имя вашего URL-шаблона

            # # Перенаправляем пользователя
            # return HttpResponseRedirect(redirect_url)

            # print('POPAL')
            # print(self.context_data)

            return render(self.request, 'add.html', self.context_data)
        elif not await self.validate_execution_fact():
            print('ПОПАЛ_44')
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
        await self.save_service(saving, execution_contract_plan, execution_contract_fact, new_service)

        query_user = await sync_to_async(lambda: ServicesVault.objects.all())()

        if not await self.total_costs(query_user, new_service):
            await self.total_costs_message()
            return render(self.request, 'add.html', self.context_data)

        from django.db.models import Q

        Services_way_ = await sync_to_async(list)(Services.objects.filter(
            Q(KOSGU=self.context_data['KOSGU']) & Q(DopFC=self.context_data['DopFC']) & Q(KTSSR=self.context_data['KTSSR']) & Q(status=self.context_data['status']) & Q(way='п.4 ч.1 ст.93')
        ))
        contract_price_sum_way = 0
        execution_contract_fact_sum_way = 0
        for service in Services_way_:
            contract_price_sum_way += await clean_number(service.contract_price if service.contract_price not in [None, 'None', ''] else 0)
            execution_contract_fact_sum_way += await clean_number(service.execution_contract_fact if service.execution_contract_fact not in [None, 'None', ''] else 0)

        ServicesVault_ = await self.validate_ServicesVault()

        ServicesVault_.off_budget_planned = await self.calculate_contract_sums('2016100092', 'Запланировано')

        ServicesVault_.budget_planned = await self.calculate_contract_sums('2016100000', 'Запланировано')

        ServicesVault_.off_budget_bargaining = await self.calculate_contract_sums('2016100092', 'В торгах')

        ServicesVault_.budget_bargaining = await self.calculate_contract_sums('2016100000', 'В торгах')

        ServicesVault_.off_budget_concluded = await self.calculate_contract_sums('2016100092', 'Заключено')

        ServicesVault_.budget_concluded = await self.calculate_contract_sums('2016100000', 'Заключено')

        ServicesVault_.off_budget_completed = await self.calculate_contract_sums('2016100092', 'Исполнено')

        ServicesVault_.budget_completed = await self.calculate_contract_sums('2016100000', 'Исполнено')

        if self.context_data['KTSSR'] == '2016100092':
            ServicesVault_.off_budget_execution = await self.calculate_contract_sums('2016100092', None)
        elif self.context_data['KTSSR'] == '2016100000':
            ServicesVault_.budget_execution = await self.calculate_contract_sums('2016100000', None)

        await sync_to_async(ServicesVault_.save)()

        ServicesVault_ = await self.validate_ServicesVault()

        await self.process_budget(ServicesVault_)

        # ServicesVault_ = await sync_to_async(ServicesVault.objects.get)(
        #     Q(KOSGU=self.context_data['KOSGU']) & Q(DopFC=self.context_data['DopFC'])
        # )

        ServicesTwo_ = await sync_to_async(ServicesTwo.objects.get)(
            Q(KOSGU=self.context_data['KOSGU']) & Q(DopFC=self.context_data['DopFC'])
        )

        await self.process_services_two(contract_price_sum_way, ServicesVault_, ServicesTwo_)

        await self.message_service_add()

        # redirect(f"/?{urlencode(self.context_data)}")

        # Кодируем query-параметры
        query_string = urlencode(self.context_data)

        # Формируем URL с query-параметрами
        redirect_url = f"{reverse('data_table_view')}?{query_string}"  # Замените 'index' на имя вашего URL-шаблона

        # Перенаправляем пользователя
        return HttpResponseRedirect(redirect_url)

        # Другие операции, такие как сохранение сервиса и т.д.

    async def process_delete(self, service):


        # KOSGU = service.KOSGU

        # DopFC = service.DopFC

        # KTSSR = service.KTSSR

        # status = service.status

        # if not await self.validate_Services():
        #     return render(self.request, 'add.html', self.context_data)
        # elif not await self.validate_ServicesVault():
        #     return render(self.request, 'add.html', self.context_data)
        # if not await self.validate_execution_plan():
        #     return render(self.request, 'add.html', self.context_data)
        # elif not await self.validate_execution_fact():
        #     return render(self.request, 'add.html', self.context_data)

        execution_contract_plan = await self.calculate_execution_plan()
        execution_contract_fact = await self.calculate_execution_fact()
        saving = await clean_number(self.context_data['NMCC']) - await clean_number(self.context_data['contract_price'])

        if await clean_number(self.context_data['contract_price']) == 0:
            self.context_data['execution'] = 0  # Или любое другое значение по умолчанию, например `None` или сообщение об ошибке
        else:
            self.context_data['execution'] = round(await clean_number(execution_contract_fact) / await clean_number(self.context_data['contract_price']), 2) * 100

        self.context_data['contract_balance'] = await clean_number(self.context_data['contract_price']) - await clean_number(execution_contract_fact)

        # new_service = Services()
        # await self.save_service(saving, execution_contract_plan, execution_contract_fact, new_service)

        # query_user = await sync_to_async(lambda: ServicesVault.objects.all())()

        # if not await self.total_costs(query_user, new_service):
        #     return render(self.request, 'add.html', self.context_data)

        from django.db.models import Q

        Services_way_ = await sync_to_async(list)(Services.objects.filter(
            Q(KOSGU=self.context_data['KOSGU']) & Q(DopFC=self.context_data['DopFC']) & Q(KTSSR=self.context_data['KTSSR']) & Q(status=self.context_data['status']) & Q(way='п.4 ч.1 ст.93')
        ))
        contract_price_sum_way = 0
        execution_contract_fact_sum_way = 0
        for service_ in Services_way_:
            contract_price_sum_way += await clean_number(service_.contract_price if service_.contract_price not in [None, 'None', ''] else 0)
            execution_contract_fact_sum_way += await clean_number(service_.execution_contract_fact if service_.execution_contract_fact not in [None, 'None', ''] else 0)

        # Удаление записи
        await sync_to_async(service.delete)()

        ServicesVault_ = await self.validate_ServicesVault()

        ServicesVault_.off_budget_planned = await self.calculate_contract_sums('2016100092', 'Запланировано')

        ServicesVault_.budget_planned = await self.calculate_contract_sums('2016100000', 'Запланировано')

        ServicesVault_.off_budget_bargaining = await self.calculate_contract_sums('2016100092', 'В торгах')

        ServicesVault_.budget_bargaining = await self.calculate_contract_sums('2016100000', 'В торгах')

        ServicesVault_.off_budget_concluded = await self.calculate_contract_sums('2016100092', 'Заключено')

        ServicesVault_.budget_concluded = await self.calculate_contract_sums('2016100000', 'Заключено')

        ServicesVault_.off_budget_completed = await self.calculate_contract_sums('2016100092', 'Исполнено')

        ServicesVault_.budget_completed = await self.calculate_contract_sums('2016100000', 'Исполнено')

        if self.context_data['KTSSR'] == '2016100092':
            ServicesVault_.off_budget_execution = await self.calculate_contract_sums('2016100092', None)
        elif self.context_data['KTSSR'] == '2016100000':
            ServicesVault_.budget_execution = await self.calculate_contract_sums('2016100000', None)

        await sync_to_async(ServicesVault_.save)()

        ServicesVault_ = await self.validate_ServicesVault()

        await self.process_budget(ServicesVault_)

        ServicesVault_ = await sync_to_async(ServicesVault.objects.get)(
            Q(KOSGU=self.context_data['KOSGU']) & Q(DopFC=self.context_data['DopFC'])
        )

        ServicesTwo_ = await sync_to_async(ServicesTwo.objects.get)(
            Q(KOSGU=self.context_data['KOSGU']) & Q(DopFC=self.context_data['DopFC'])
        )

        await self.process_services_two(contract_price_sum_way, ServicesVault_, ServicesTwo_)

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
            # data = request.POST

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

            # # Создаем список месяцев
            # months = [
            #     context_data['january_one'], context_data['february'], context_data['march'], context_data['april'], context_data['may'], context_data['june'],
            #     context_data['july'], context_data['august'], context_data['september'], context_data['october'], context_data['november'], context_data['december'],
            #     context_data['january_two']
            # ]

            # # Асинхронно обрабатываем все месяцы
            # cleaned_numbers = await asyncio.gather(*(clean_number(month) for month in months))

            # # Суммируем результат
            # execution_contract_plan = sum(cleaned_numbers)

            # if context_data['contract_price']:
            #     if f"{execution_contract_plan:g}" != context_data['contract_price']:
            #         await sync_to_async(messages.error)(request, 'Значение поля «Исполнение контракта (план) должно равняться полю «Цена контракта»')

            #         return render(request, 'edit.html', context_data)

            # # Создаем список сумм месяцев
            # sum_months = [
            #     context_data['sum_january_one'], context_data['sum_february'], context_data['sum_march'], context_data['sum_april'], context_data['sum_may'], context_data['sum_june'],
            #     context_data['sum_july'], context_data['sum_august'], context_data['sum_september'], context_data['sum_october'], context_data['sum_november'], context_data['sum_december'],
            #     context_data['sum_january_two']
            # ]

            # # Асинхронно обрабатываем все месяцы
            # cleaned_numbers = await asyncio.gather(*(clean_number(month) for month in sum_months))

            # # Суммируем результат
            # execution_contract_fact = sum(cleaned_numbers)

            # if execution_contract_plan != execution_contract_fact and context_data['status'] == 'Исполнено':
            #     await sync_to_async(messages.error)(request, 'Нельзя выставить статус "Исполнено" при неравенстве ячеек «Исполнение контракта (факт)» и «Исполнение контракта (план)»')

            #     return render(request, 'edit.html', context_data)

            # saving = await clean_number(context_data['NMCC']) - await clean_number(context_data['contract_price'])

            # if await clean_number(context_data['contract_price']) == 0:
            #     context_data['execution'] = 0  # Или любое другое значение по умолчанию, например `None` или сообщение об ошибке
            # else:
            #     context_data['execution'] = round(await clean_number(execution_contract_fact) / await clean_number(context_data['contract_price']), 2) * 100

            # context_data['contract_balance'] = await clean_number(context_data['contract_price']) - await clean_number(execution_contract_fact)

            # from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

            # try:
            #     Services_ = await sync_to_async(Services.objects.get)(name=context_data['name'])

            # except MultipleObjectsReturned:
            #     Services_ = await sync_to_async(lambda: Services.objects.filter(name=context_data['name']).first())()
            #     await sync_to_async(messages.error)(request, 'Вы добавляете дубликат в Наименовании')

            #     return render(request, 'edit.html', context_data)
            # except ObjectDoesNotExist:
            #     pass

            # try:
            #     from django.db.models import Q

            #     ServicesVault_ = await sync_to_async(ServicesVault.objects.get)(
            #         Q(KOSGU=context_data['KOSGU']) & Q(DopFC=context_data['DopFC'])
            #     )
            # except:
            #     await sync_to_async(messages.error)(request, 'Нет сопоставления КОСГУ с ДопФК')

            #     return render(request, 'edit.html', context_data)

            # context_data['service'].id_id = context_data['id_id']
            # context_data['service'].name = context_data['name']
            # context_data['service'].status = context_data['status']
            # context_data['service'].way = context_data['way']
            # context_data['service'].initiator = context_data['initiator']
            # context_data['service'].KTSSR = context_data['KTSSR']
            # context_data['service'].KOSGU = context_data['KOSGU']
            # context_data['service'].DopFC = context_data['DopFC']
            # context_data['service'].NMCC = context_data['NMCC']
            # context_data['service'].saving = saving
            # context_data['service'].counterparty = context_data['counterparty']
            # context_data['service'].registration_number = context_data['registration_number']
            # context_data['service'].contract_number = context_data['contract_number']
            # context_data['service'].contract_date = context_data['contract_date']
            # context_data['service'].end_date = context_data['end_date']
            # context_data['service'].contract_price = context_data['contract_price']
            # context_data['service'].execution_contract_plan = execution_contract_plan
            # context_data['service'].january_one = context_data['january_one']
            # context_data['service'].february = context_data['february']
            # context_data['service'].march = context_data['march']
            # context_data['service'].april = context_data['april']
            # context_data['service'].may = context_data['may']
            # context_data['service'].june = context_data['june']
            # context_data['service'].july = context_data['july']
            # context_data['service'].august = context_data['august']
            # context_data['service'].september = context_data['september']
            # context_data['service'].october = context_data['october']
            # context_data['service'].november = context_data['november']
            # context_data['service'].december = context_data['december']
            # context_data['service'].january_two = context_data['january_two']
            # context_data['service'].execution_contract_fact = execution_contract_fact
            # context_data['service'].date_january_one = context_data['date_january_one']
            # context_data['service'].sum_january_one = context_data['sum_january_one']
            # context_data['service'].date_february = context_data['date_february']
            # context_data['service'].sum_february = context_data['sum_february']
            # context_data['service'].date_march = context_data['date_march']
            # context_data['service'].sum_march = context_data['sum_march']
            # context_data['service'].date_april = context_data['date_april']
            # context_data['service'].sum_april = context_data['sum_april']
            # context_data['service'].date_may = context_data['date_may']
            # context_data['service'].sum_may = context_data['sum_may']
            # context_data['service'].date_june = context_data['date_june']
            # context_data['service'].sum_june = context_data['sum_june']
            # context_data['service'].date_july = context_data['date_july']
            # context_data['service'].sum_july = context_data['sum_july']
            # context_data['service'].date_august = context_data['date_august']
            # context_data['service'].sum_august = context_data['sum_august']
            # context_data['service'].date_september = context_data['date_september']
            # context_data['service'].sum_september = context_data['sum_september']
            # context_data['service'].date_october = context_data['date_october']
            # context_data['service'].sum_october = context_data['sum_october']
            # context_data['service'].date_november = context_data['date_november']
            # context_data['service'].sum_november = context_data['sum_november']
            # context_data['service'].date_december = context_data['date_december']
            # context_data['service'].sum_december = context_data['sum_december']
            # context_data['service'].date_january_two = context_data['date_january_two']
            # context_data['service'].sum_january_two = context_data['sum_january_two']
            # context_data['service'].execution = context_data['execution']
            # context_data['service'].contract_balance = context_data['contract_balance']
            # context_data['service'].color = context_data['color']

            # await sync_to_async(context_data['service'].save)()

            # Services_2016100000_ = await sync_to_async(list)(Services.objects.filter(
            #     Q(KOSGU=context_data['KOSGU']) & Q(DopFC=context_data['DopFC']) & Q(KTSSR='2016100000')
            # ))

            # execution_contract_fact_sum_2016100000 = 0
            # for service in Services_2016100000_:
            #     execution_contract_fact_sum_2016100000 += await clean_number(service.execution_contract_fact if service.execution_contract_fact not in [None, 'None', ''] else 0)

            # Services_2016100092_ = await sync_to_async(list)(Services.objects.filter(
            #     Q(KOSGU=context_data['KOSGU']) & Q(DopFC=context_data['DopFC']) & Q(KTSSR='2016100092')
            # ))

            # execution_contract_fact_sum_2016100092 = 0
            # for service in Services_2016100092_:
            #     execution_contract_fact_sum_2016100092 += await clean_number(service.execution_contract_fact if service.execution_contract_fact not in [None, 'None', ''] else 0)

            # Services_planned_2016100000_ = await sync_to_async(list)(Services.objects.filter(
            #     Q(KOSGU=context_data['KOSGU']) & Q(DopFC=context_data['DopFC']) & Q(KTSSR='2016100000') & Q(status='Запланировано')
            # ))

            # contract_price_sum_planned_2016100000 = 0
            # for service in Services_planned_2016100000_:
            #     contract_price_sum_planned_2016100000 += await clean_number(service.contract_price if service.contract_price not in [None, 'None', ''] else 0)

            # Services_off_planned_2016100092_ = await sync_to_async(list)(Services.objects.filter(
            #     Q(KOSGU=context_data['KOSGU']) & Q(DopFC=context_data['DopFC']) & Q(KTSSR='2016100092') & Q(status='Запланировано')
            # ))

            # contract_price_sum_off_planned_2016100092 = 0
            # for service in Services_off_planned_2016100092_:
            #     contract_price_sum_off_planned_2016100092 += await clean_number(service.contract_price if service.contract_price not in [None, 'None', ''] else 0)

            # Services_bargaining_2016100000_ = await sync_to_async(list)(Services.objects.filter(
            #     Q(KOSGU=context_data['KOSGU']) & Q(DopFC=context_data['DopFC']) & Q(KTSSR='2016100000') & Q(status='В торгах')
            # ))

            # contract_price_sum_bargaining_2016100000 = 0
            # for service in Services_bargaining_2016100000_:
            #     contract_price_sum_bargaining_2016100000 += await clean_number(service.contract_price if service.contract_price not in [None, 'None', ''] else 0)

            # Services_off_bargaining_2016100092_ = await sync_to_async(list)(Services.objects.filter(
            #     Q(KOSGU=context_data['KOSGU']) & Q(DopFC=context_data['DopFC']) & Q(KTSSR='2016100092') & Q(status='В торгах')
            # ))

            # contract_price_sum_off_bargaining_2016100092 = 0
            # for service in Services_off_bargaining_2016100092_:
            #     contract_price_sum_off_bargaining_2016100092 += await clean_number(service.contract_price if service.contract_price not in [None, 'None', ''] else 0)

            # Services_concluded_2016100000_ = await sync_to_async(list)(Services.objects.filter(
            #     Q(KOSGU=context_data['KOSGU']) & Q(DopFC=context_data['DopFC']) & Q(KTSSR='2016100000') & Q(status='Заключено')
            # ))

            # contract_price_sum_concluded_2016100000 = 0
            # for service in Services_concluded_2016100000_:
            #     contract_price_sum_concluded_2016100000 += await clean_number(service.contract_price if service.contract_price not in [None, 'None', ''] else 0)

            # Services_off_concluded_2016100092_ = await sync_to_async(list)(Services.objects.filter(
            #     Q(KOSGU=context_data['KOSGU']) & Q(DopFC=context_data['DopFC']) & Q(KTSSR='2016100092') & Q(status='Заключено')
            # ))

            # contract_price_sum_off_concluded_2016100092 = 0
            # for service in Services_off_concluded_2016100092_:
            #     contract_price_sum_off_concluded_2016100092 += await clean_number(service.contract_price if service.contract_price not in [None, 'None', ''] else 0)

            # Services_completed_2016100000_ = await sync_to_async(list)(Services.objects.filter(
            #     Q(KOSGU=context_data['KOSGU']) & Q(DopFC=context_data['DopFC']) & Q(KTSSR='2016100000') & Q(status='Исполнено')
            # ))

            # contract_price_sum_completed_2016100000 = 0
            # for service in Services_completed_2016100000_:
            #     contract_price_sum_completed_2016100000 += await clean_number(service.contract_price if service.contract_price not in [None, 'None', ''] else 0)

            # Services_off_completed_2016100092_ = await sync_to_async(list)(Services.objects.filter(
            #     Q(KOSGU=context_data['KOSGU']) & Q(DopFC=context_data['DopFC']) & Q(KTSSR='2016100092') & Q(status='Исполнено')
            # ))

            # contract_price_sum_off_completed_2016100092 = 0
            # for service in Services_off_completed_2016100092_:
            #     contract_price_sum_off_completed_2016100092 += await clean_number(service.contract_price if service.contract_price not in [None, 'None', ''] else 0)

            # Services_way_ = await sync_to_async(list)(Services.objects.filter(
            #     Q(KOSGU=context_data['KOSGU']) & Q(DopFC=context_data['DopFC']) & Q(KTSSR=context_data['KTSSR']) & Q(status=context_data['status']) & Q(way='п.4 ч.1 ст.93')
            # ))
            # contract_price_sum_way = 0
            # execution_contract_fact_sum_way = 0
            # for service in Services_way_:
            #     contract_price_sum_way += await clean_number(service.contract_price if service.contract_price not in [None, 'None', ''] else 0)
            #     execution_contract_fact_sum_way += await clean_number(service.execution_contract_fact if service.execution_contract_fact not in [None, 'None', ''] else 0)

            # ServicesVault_.off_budget_planned = contract_price_sum_off_planned_2016100092

            # ServicesVault_.budget_planned = contract_price_sum_planned_2016100000

            # ServicesVault_.off_budget_bargaining = contract_price_sum_off_bargaining_2016100092

            # ServicesVault_.budget_bargaining = contract_price_sum_bargaining_2016100000

            # ServicesVault_.off_budget_concluded = contract_price_sum_off_concluded_2016100092

            # ServicesVault_.budget_concluded = contract_price_sum_concluded_2016100000

            # ServicesVault_.off_budget_completed = contract_price_sum_off_completed_2016100092

            # ServicesVault_.budget_completed = contract_price_sum_completed_2016100000

            # if context_data['KTSSR'] == '2016100092':
            #     ServicesVault_.off_budget_execution = execution_contract_fact_sum_2016100092
            # elif context_data['KTSSR'] == '2016100000':
            #     ServicesVault_.budget_execution = execution_contract_fact_sum_2016100000

            # await sync_to_async(ServicesVault_.save)()

            # try:
            #     from django.db.models import Q

            #     ServicesVault_ = await sync_to_async(ServicesVault.objects.get)(
            #         Q(KOSGU=context_data['KOSGU']) & Q(DopFC=context_data['DopFC'])
            #     )
            # except:
            #     await sync_to_async(messages.error)(request, 'Нет сопоставления КОСГУ с ДопФК')

            #     return render(request, 'edit.html', context_data)

            # # Создаем список месяцев
            # budget = [
            #     ServicesVault_.budget_limit if ServicesVault_.budget_limit not in [None, 'None', ''] else 0,
            #     ServicesVault_.budget_bargaining if ServicesVault_.budget_bargaining not in [None, 'None', ''] else 0,
            #     ServicesVault_.budget_concluded if ServicesVault_.budget_concluded not in [None, 'None', ''] else 0,
            #     ServicesVault_.budget_completed if ServicesVault_.budget_completed not in [None, 'None', ''] else 0
            # ]

            # # Асинхронно обрабатываем все месяцы
            # cleaned_numbers = await asyncio.gather(*(clean_number(number) for number in budget))

            # # Суммируем результат
            # ServicesVault_.budget_remainder = cleaned_numbers[0] - sum(cleaned_numbers[1:])

            # # Создаем список месяцев
            # off_budget = [
            #     ServicesVault_.off_budget_limit if ServicesVault_.off_budget_limit not in [None, 'None', ''] else 0,
            #     ServicesVault_.off_budget_bargaining if ServicesVault_.off_budget_bargaining not in [None, 'None', ''] else 0,
            #     ServicesVault_.off_budget_concluded if ServicesVault_.off_budget_concluded not in [None, 'None', ''] else 0,
            #     ServicesVault_.off_budget_completed if ServicesVault_.off_budget_completed not in [None, 'None', ''] else 0
            # ]

            # # Асинхронно обрабатываем все месяцы
            # cleaned_numbers = await asyncio.gather(*(clean_number(number) for number in off_budget))

            # # Суммируем результат
            # ServicesVault_.off_budget_remainder = cleaned_numbers[0] - sum(cleaned_numbers[1:])

            # ServicesVault_.budget_plans = await clean_number(ServicesVault_.budget_remainder if ServicesVault_.budget_remainder not in [None, 'None', ''] else 0) - await clean_number(ServicesVault_.budget_planned if ServicesVault_.budget_planned not in [None, 'None', ''] else 0)
            # ServicesVault_.off_budget_plans = await clean_number(ServicesVault_.off_budget_remainder if ServicesVault_.off_budget_remainder not in [None, 'None', ''] else 0) - await clean_number(ServicesVault_.off_budget_planned if ServicesVault_.off_budget_planned not in [None, 'None', ''] else 0)

            # if any(x < 0 for x in [await clean_number(ServicesVault_.budget_remainder),
            #                     await clean_number(ServicesVault_.off_budget_remainder),
            #                     await clean_number(ServicesVault_.budget_plans),
            #                     await clean_number(ServicesVault_.off_budget_plans)]):
            #     ServicesVault_.color = '#ffebeb'
            # else:
            #     ServicesVault_.color = ''

            # await sync_to_async(ServicesVault_.save)()

            # try:
            #     from django.db.models import Q

            #     ServicesTwo_ = await sync_to_async(ServicesTwo.objects.get)(
            #         Q(KOSGU=context_data['KOSGU']) & Q(DopFC=context_data['DopFC'])
            #     )

            #     ServicesVault_ = await sync_to_async(ServicesVault.objects.get)(
            #         Q(KOSGU=context_data['KOSGU']) & Q(DopFC=context_data['DopFC'])
            #     )

            #     if context_data['status'] == 'Заключено' and context_data['KTSSR'] == '2016100092':
            #         ServicesTwo_.off_budget_concluded = contract_price_sum_way
            #         ServicesTwo_.off_budget_remainder = await clean_number(ServicesVault_.off_budget_planned) - await clean_number(contract_price_sum_way)
            #     elif context_data['status'] == 'Заключено' and context_data['KTSSR'] == '2016100000':
            #         ServicesTwo_.budget_concluded = contract_price_sum_way
            #         ServicesTwo_.budget_remainder = await clean_number(ServicesVault_.budget_planned) - await clean_number(contract_price_sum_way)

            #     if any(x < 0 for x in [await clean_number(ServicesVault_.budget_remainder), await clean_number(ServicesVault_.off_budget_remainder), await clean_number(ServicesVault_.budget_plans), await clean_number(ServicesVault_.off_budget_plans)]):
            #         ServicesTwo_.color = '#ffebeb'
            #     else:
            #         ServicesTwo_.color = ''

            #     await sync_to_async(ServicesTwo_.save)()

            # except Exception as e:
            #     # Вывод подробной информации об ошибке
            #     print(f"Поймано исключение: {type(e).__name__}")
            #     print(f"Сообщение об ошибке: {str(e)}")
            #     import traceback
            #     print("Трассировка стека (stack trace):")
            #     traceback.print_exc()

            # await sync_to_async(messages.success)(request, "Редактирование прошло успешно.")

            # # Перенаправление с несколькими параметрами
            # return redirect(f"/?{urlencode(context_data)}")

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
                'service_user': await sync_to_async(ServicesVault.objects.get)(id=row_id),
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

            # data = request.POST

            # id_id = data.get('id_id')
            # name = data.get('name')
            # KOSGU = data.get('KOSGU')
            # DopFC = data.get('DopFC')
            # budget_limit = data.get('budget_limit')
            # off_budget_limit = data.get('off_budget_limit')
            # budget_planned = data.get('budget_planned')
            # off_budget_planned = data.get('off_budget_planned')
            # budget_bargaining = data.get('budget_bargaining')
            # off_budget_bargaining = data.get('off_budget_bargaining')
            # budget_concluded = data.get('budget_concluded')
            # off_budget_concluded = data.get('off_budget_concluded')
            # budget_completed = data.get('budget_completed')
            # off_budget_completed = data.get('off_budget_completed')
            # budget_execution = data.get('budget_execution')
            # off_budget_execution = data.get('off_budget_execution')
            # budget_remainder = data.get('budget_remainder')
            # off_budget_remainder = data.get('off_budget_remainder')
            # budget_plans = data.get('budget_plans')
            # off_budget_plans = data.get('off_budget_plans')
            # color = data.get('color')

            # # Найдите запись по ID и обновите цвет
            # service = await sync_to_async(ServicesVault.objects.get)(id=row_id)

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

            # try:
            #     from django.db.models import Q

            #     ServicesVault_ = await sync_to_async(ServicesVault.objects.get)(
            #         Q(KOSGU=KOSGU) & Q(DopFC=DopFC)
            #     )

            #     # Создаем список месяцев
            #     budget = [
            #         ServicesVault_.budget_limit if ServicesVault_.budget_limit not in [None, 'None', ''] else 0,
            #         ServicesVault_.budget_bargaining if ServicesVault_.budget_bargaining not in [None, 'None', ''] else 0,
            #         ServicesVault_.budget_concluded if ServicesVault_.budget_concluded not in [None, 'None', ''] else 0,
            #         ServicesVault_.budget_completed if ServicesVault_.budget_completed not in [None, 'None', ''] else 0
            #     ]

            #     # Асинхронно обрабатываем все месяцы
            #     cleaned_numbers = await asyncio.gather(*(clean_number(number) for number in budget))

            #     # Суммируем результат
            #     ServicesVault_.budget_remainder = cleaned_numbers[0] - sum(cleaned_numbers[1:])

            #     # Создаем список месяцев
            #     off_budget = [
            #         ServicesVault_.off_budget_limit if ServicesVault_.off_budget_limit not in [None, 'None', ''] else 0,
            #         ServicesVault_.off_budget_bargaining if ServicesVault_.off_budget_bargaining not in [None, 'None', ''] else 0,
            #         ServicesVault_.off_budget_concluded if ServicesVault_.off_budget_concluded not in [None, 'None', ''] else 0,
            #         ServicesVault_.off_budget_completed if ServicesVault_.off_budget_completed not in [None, 'None', ''] else 0
            #     ]

            #     # Асинхронно обрабатываем все месяцы
            #     cleaned_numbers = await asyncio.gather(*(clean_number(number) for number in off_budget))

            #     # Суммируем результат
            #     ServicesVault_.off_budget_remainder = sum(cleaned_numbers)

            #     await sync_to_async(ServicesVault_.save)()
            # except Exception as e:
            #     # Вывод подробной информации об ошибке
            #     print(f"Поймано исключение: {type(e).__name__}")
            #     print(f"Сообщение об ошибке: {str(e)}")
            #     import traceback
            #     print("Трассировка стека (stack trace):")
            #     traceback.print_exc()

            # await sync_to_async(messages.success)(request, "Редактирование прошло успешно.")

            # page = 1
            # keyword_one = None
            # keyword_two = None
            # selected_column_one = None
            # selected_column_two = None

            # page_user = int(request.GET.get('page_user', 1))
            # KOSGU_user = request.GET.get('KOSGU_user', None)
            # keyword_one_user = request.GET.get('keyword_one_user', None)
            # keyword_two_user = request.GET.get('keyword_two_user', None)
            # selected_column_one_user = request.GET.get('selected_column_one_user', None)
            # selected_column_two_user = request.GET.get('selected_column_two_user', None)

            # page_user_two = int(request.GET.get('page_user_two', 1))
            # KOSGU_user_two = request.GET.get('KOSGU_user_two', None)
            # keyword_one_user_two = request.GET.get('keyword_one_user_two', None)
            # keyword_two_user_two = request.GET.get('keyword_two_user_two', None)
            # selected_column_one_user_two = request.GET.get('selected_column_one_user_two', None)
            # selected_column_two_user_two = request.GET.get('selected_column_two_user_two', None)

            # # Формирование строки запроса
            # query_params = {
            #     'page': page,
            #     'keyword_one': keyword_one,
            #     'keyword_two': keyword_two,
            #     'selected_column_one': selected_column_one,
            #     'selected_column_two': selected_column_two,
            #     'page_user': page_user,
            #     'KOSGU_user': KOSGU_user,
            #     'keyword_one_user': keyword_one_user,
            #     'keyword_two_user': keyword_two_user,
            #     'selected_column_one_user': selected_column_one_user,
            #     'selected_column_two_user': selected_column_two_user,
            #     'page_user_two': page_user_two,
            #     'KOSGU_user_two': KOSGU_user_two,
            #     'keyword_one_user_two': keyword_one_user_two,
            #     'keyword_two_user_two': keyword_two_user_two,
            #     'selected_column_one_user_two': selected_column_one_user_two,
            #     'selected_column_two_user_two': selected_column_two_user_two
            # }

            # # Перенаправление с несколькими параметрами
            # return redirect(f"/?{urlencode(query_params)}")

        except Services.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Service not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON.'}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)

@csrf_exempt  # Необходимо, если вы не используете CSRF-токены
async def update_record_user_two(request, row_id):
    if request.method == 'POST':
        try:
            data = request.POST

            id_id = data.get('id_id')
            KOSGU = data.get('KOSGU')
            DopFC = data.get('DopFC')
            budget_planned = data.get('budget_planned')
            off_budget_planned = data.get('off_budget_planned')
            budget_concluded = data.get('budget_concluded')
            off_budget_concluded = data.get('off_budget_concluded')
            budget_remainder = data.get('budget_remainder')
            off_budget_remainder = data.get('off_budget_remainder')
            color = data.get('color')

            # Найдите запись по ID и обновите цвет
            service = await sync_to_async(ServicesTwo.objects.get)(id=row_id)

            service.id_id = id_id
            service.KOSGU = KOSGU
            service.budget_planned = budget_planned
            service.off_budget_planned = off_budget_planned
            service.budget_concluded = budget_concluded
            service.off_budget_concluded = off_budget_concluded
            service.budget_remainder = budget_remainder
            service.off_budget_remainder = off_budget_remainder
            service.color = color

            await sync_to_async(service.save)()

            try:
                from django.db.models import Q

                ServicesTwo_ = await sync_to_async(ServicesTwo.objects.get)(
                    Q(KOSGU=KOSGU) & Q(DopFC=DopFC)
                )

                ServicesTwo_.budget_plans = await clean_number(ServicesTwo_.budget_remainder if ServicesTwo_.budget_remainder not in [None, 'None', ''] else 0) - await clean_number(ServicesTwo_.budget_planned if ServicesTwo_.budget_planned not in [None, 'None', ''] else 0)
                ServicesTwo_.off_budget_plans = await clean_number(ServicesTwo_.off_budget_remainder if ServicesTwo_.off_budget_remainder not in [None, 'None', ''] else 0) - await clean_number(ServicesTwo_.off_budget_planned if ServicesTwo_.off_budget_planned not in [None, 'None', ''] else 0)

                await sync_to_async(ServicesTwo_.save)()

            except Exception as e:
                # Вывод подробной информации об ошибке
                print(f"Поймано исключение: {type(e).__name__}")
                print(f"Сообщение об ошибке: {str(e)}")
                import traceback
                print("Трассировка стека (stack trace):")
                traceback.print_exc()

            await sync_to_async(messages.success)(request, "Редактирование прошло успешно.")

            page = 1
            keyword_one = None
            keyword_two = None
            selected_column_one = None
            selected_column_two = None

            page_user = int(request.GET.get('page_user', 1))
            KOSGU_user = request.GET.get('KOSGU_user', None)
            keyword_one_user = request.GET.get('keyword_one_user', None)
            keyword_two_user = request.GET.get('keyword_two_user', None)
            selected_column_one_user = request.GET.get('selected_column_one_user', None)
            selected_column_two_user = request.GET.get('selected_column_two_user', None)

            page_user_two = int(request.GET.get('page_user_two', 1))
            KOSGU_user_two = request.GET.get('KOSGU_user_two', None)
            keyword_one_user_two = request.GET.get('keyword_one_user_two', None)
            keyword_two_user_two = request.GET.get('keyword_two_user_two', None)
            selected_column_one_user_two = request.GET.get('selected_column_one_user_two', None)
            selected_column_two_user_two = request.GET.get('selected_column_two_user_two', None)

            # Формирование строки запроса
            query_params = {
                'page': page,
                'keyword_one': keyword_one,
                'keyword_two': keyword_two,
                'selected_column_one': selected_column_one,
                'selected_column_two': selected_column_two,
                'page_user': page_user,
                'KOSGU_user': KOSGU_user,
                'keyword_one_user': keyword_one_user,
                'keyword_two_user': keyword_two_user,
                'selected_column_one_user': selected_column_one_user,
                'selected_column_two_user': selected_column_two_user,
                'page_user_two': page_user_two,
                'KOSGU_user_two': KOSGU_user_two,
                'keyword_one_user_two': keyword_one_user_two,
                'keyword_two_user_two': keyword_two_user_two,
                'selected_column_one_user_two': selected_column_one_user_two,
                'selected_column_two_user_two': selected_column_two_user_two
            }

            # Перенаправление с несколькими параметрами
            return redirect(f"/?{urlencode(query_params)}")

        except Services.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Service not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON.'}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)

@csrf_exempt  # Необходимо, если вы не используете CSRF-токены
async def add_record(request):

    if request.method == 'POST':
        try:

            # # Возвращаем данные формы обратно в шаблон
            # context_data = {
            #     'name': request.POST['name'],
            #     'status': request.POST['status'],
            #     'way': request.POST['way'],
            #     'initiator': request.POST['initiator'],
            #     'KTSSR': request.POST['KTSSR'],
            #     'KOSGU': request.POST['KOSGU'],
            #     'DopFC': request.POST['DopFC'],
            #     'NMCC': request.POST['NMCC'],
            #     'counterparty': request.POST['counterparty'],
            #     'registration_number': request.POST['registration_number'],
            #     'contract_number': request.POST['contract_number'],
            #     'contract_date': request.POST['contract_date'],
            #     'end_date': request.POST['end_date'],
            #     'contract_price': request.POST['contract_price'],
            #     'january_one': request.POST['january_one'],
            #     'february': request.POST['february'],
            #     'march': request.POST['march'],
            #     'april': request.POST['april'],
            #     'may': request.POST['may'],
            #     'june': request.POST['june'],
            #     'july': request.POST['july'],
            #     'august': request.POST['august'],
            #     'september': request.POST['september'],
            #     'october': request.POST['october'],
            #     'november': request.POST['november'],
            #     'december': request.POST['december'],
            #     'january_two': request.POST['january_two'],
            #     'date_january_one': request.POST['date_january_one'],
            #     'sum_january_one': request.POST['sum_january_one'],
            #     'date_february': request.POST['date_february'],
            #     'sum_february': request.POST['sum_february'],
            #     'date_march': request.POST['date_march'],
            #     'sum_march':  request.POST['sum_march'],
            #     'date_april': request.POST['date_april'],
            #     'sum_april': request.POST['sum_april'],
            #     'date_may': request.POST['date_may'],
            #     'sum_may': request.POST['sum_may'],
            #     'date_june': request.POST['date_june'],
            #     'sum_june': request.POST['sum_june'],
            #     'date_july': request.POST['date_july'],
            #     'sum_july': request.POST['sum_july'],
            #     'date_august': request.POST['date_august'],
            #     'sum_august': request.POST['sum_august'],
            #     'date_september': request.POST['date_september'],
            #     'sum_september': request.POST['sum_september'],
            #     'date_october': request.POST['date_october'],
            #     'sum_october': request.POST['sum_october'],
            #     'date_november': request.POST['date_november'],
            #     'sum_november': request.POST['sum_november'],
            #     'date_december': request.POST['date_december'],
            #     'sum_december': request.POST['sum_december'],
            #     'date_january_two': request.POST['date_january_two'],
            #     'sum_january_two': request.POST['sum_january_two'],
            #     'execution': request.POST['execution'],
            #     'contract_balance': request.POST['contract_balance'],
            #     'execution_contract_fact': request.POST['execution_contract_fact'],
            #     'execution_contract_plan': request.POST['execution_contract_plan'],
            #     'saving': request.POST['saving'],
            #     'color': request.POST['color'],
            #     'page': int(request.GET.get('total_pages', 1)),
            #     'keyword_one': request.GET.get('keyword_one', None),
            #     'keyword_two': request.GET.get('keyword_two', None),
            #     'selected_column_one': request.GET.get('selected_column_one', None),
            #     'selected_column_two': request.GET.get('selected_column_two', None),
            #     'page_user': 1,
            #     'KOSGU_user': request.GET.get('KOSGU_user', None),
            #     'keyword_one_user': request.GET.get('keyword_one_user', None),
            #     'keyword_two_user': request.GET.get('keyword_two_user', None),
            #     'selected_column_one_user': request.GET.get('selected_column_one_user', None),
            #     'selected_column_two_user': request.GET.get('selected_column_two_user', None),
            #     'page_user_two': 1,
            #     'KOSGU_user_two': request.GET.get('KOSGU_user_two', None),
            #     'keyword_one_user_two': request.GET.get('keyword_one_user_two', None),
            #     'keyword_two_user_two': request.GET.get('keyword_two_user_two', None),
            #     'selected_column_one_user_two': request.GET.get('selected_column_one_user_two', None),
            #     'selected_column_two_user_two': request.GET.get('selected_column_two_user_two', None)
            # }

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

            # # Создаем список месяцев
            # months = [
            #     context_data['january_one'], context_data['february'], context_data['march'], context_data['april'], context_data['may'], context_data['june'],
            #     context_data['july'], context_data['august'], context_data['september'], context_data['october'], context_data['november'], context_data['december'],
            #     context_data['january_two']
            # ]

            # # Асинхронно обрабатываем все месяцы
            # cleaned_numbers = await asyncio.gather(*(clean_number(month) for month in months))

            # # Суммируем результат
            # execution_contract_plan = sum(cleaned_numbers)

            # if context_data['contract_price']:
            #     if f"{execution_contract_plan:g}" != context_data['contract_price']:
            #         await sync_to_async(messages.error)(request, 'Значение поля «Исполнение контракта (план) должно равняться полю «Цена контракта»')

            #         return render(request, 'add.html', context_data)

            # # Создаем список сумм месяцев
            # sum_months = [
            #     context_data['sum_january_one'], context_data['sum_february'], context_data['sum_march'], context_data['sum_april'], context_data['sum_may'], context_data['sum_june'],
            #     context_data['sum_july'], context_data['sum_august'], context_data['sum_september'], context_data['sum_october'], context_data['sum_november'], context_data['sum_december'],
            #     context_data['sum_january_two']
            # ]

            # # Асинхронно обрабатываем все месяцы
            # cleaned_numbers = await asyncio.gather(*(clean_number(month) for month in sum_months))

            # # Суммируем результат
            # execution_contract_fact = sum(cleaned_numbers)

            # if execution_contract_plan != execution_contract_fact and context_data['status'] == 'Исполнено':
            #     await sync_to_async(messages.error)(request, 'Нельзя выставить статус "Исполнено" при неравенстве ячеек «Исполнение контракта (факт)» и «Исполнение контракта (план)»')

            #     return render(request, 'add.html', context_data)

            # saving = await clean_number(context_data['NMCC']) - await clean_number(context_data['contract_price'])

            # if await clean_number(context_data['contract_price']) == 0:
            #     context_data['execution'] = 0  # Или любое другое значение по умолчанию, например `None` или сообщение об ошибке
            # else:
            #     context_data['execution'] = round(await clean_number(execution_contract_fact) / await clean_number(context_data['contract_price']), 2) * 100

            # contract_balance = await clean_number(context_data['contract_price']) - await clean_number(execution_contract_fact)

            # from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

            # try:
            #     Services_ = await sync_to_async(Services.objects.get)(name=context_data['name'])
            #     await sync_to_async(messages.error)(request, 'Вы добавляете дубликат в Наименовании')

            #     return render(request, 'add.html', context_data)
            # except MultipleObjectsReturned:
            #     Services_ = await sync_to_async(lambda: Services.objects.filter(name=context_data['name']).first())()
            #     await sync_to_async(messages.error)(request, 'Вы добавляете дубликат в Ниименовании')

            #     return render(request, 'add.html', context_data)
            # except ObjectDoesNotExist:
            #     pass

            # # Получаем следующий ID
            # from django.db import connection

            # def get_latest_service():
            #     with connection.cursor() as cursor:
            #         cursor.execute("""
            #             SELECT id_id FROM services_base
            #             WHERE id_id REGEXP '^[0-9]+$'
            #             ORDER BY CAST(id_id AS UNSIGNED) DESC
            #             LIMIT 1
            #         """)
            #         row = cursor.fetchone()
            #         return row

            # latest_service = await sync_to_async(get_latest_service)()

            # try:
            #     id_id = (int(latest_service[0]) + 1) if latest_service and latest_service[0].isdigit() else 1
            # except ValueError:
            #     # В случае некорректного значения установить id_id на 1
            #     id_id = 1

            # new_service = Services(id_id=id_id, name=context_data['name'], status=context_data['status'], way=context_data['way'],
            #                     initiator=context_data['initiator'], KTSSR=context_data['KTSSR'], KOSGU=context_data['KOSGU'],
            #                     DopFC=context_data['DopFC'], NMCC=context_data['NMCC'], saving=saving,
            #                     counterparty=context_data['counterparty'], registration_number=context_data['registration_number'],
            #                     contract_number=context_data['contract_number'], contract_date=context_data['contract_date'],
            #                     end_date=context_data['end_date'], contract_price=context_data['contract_price'], execution_contract_plan=execution_contract_plan,
            #                     january_one=context_data['january_one'], february=context_data['february'], march=context_data['march'], april=context_data['april'],
            #                     may=context_data['may'], june=context_data['june'], july=context_data['july'], august=context_data['august'],
            #                     september=context_data['september'], october=context_data['october'], november=context_data['november'], december=context_data['december'],
            #                     january_two=context_data['january_two'], execution_contract_fact=execution_contract_fact, date_january_one=context_data['date_january_one'],
            #                     sum_january_one=context_data['sum_january_one'], date_february=context_data['date_february'], sum_february=context_data['sum_february'],
            #                     date_march=context_data['date_march'], sum_march=context_data['sum_march'], date_april=context_data['date_april'],
            #                     sum_april=context_data['sum_april'], date_may=context_data['date_may'], sum_may=context_data['sum_may'],
            #                     date_june=context_data['date_june'], sum_june=context_data['sum_june'], date_july=context_data['date_july'],
            #                     sum_july=context_data['sum_july'], date_august=context_data['date_august'], sum_august=context_data['sum_august'],
            #                     date_september=context_data['date_september'], sum_september=context_data['sum_september'], date_october=context_data['date_october'],
            #                     sum_october=context_data['sum_october'], date_november=context_data['date_november'], sum_november=context_data['sum_november'],
            #                     date_december=context_data['date_december'], sum_december=context_data['sum_december'], date_january_two=context_data['date_january_two'],
            #                     sum_january_two=context_data['sum_january_two'], execution=context_data['execution'], contract_balance=contract_balance,
            #                     color=context_data['color'])

            # await sync_to_async(new_service.save)()

            # query_user = await sync_to_async(lambda: ServicesVault.objects.all())()

            # total_cost_1 = await sync_to_async(lambda: query_user.aggregate(Sum('budget_limit')))()
            # total_cost_1 = total_cost_1['budget_limit__sum'] or 0
            # total_cost_2 = await sync_to_async(lambda: query_user.aggregate(Sum('off_budget_limit')))()
            # total_cost_2 = total_cost_2['off_budget_limit__sum'] or 0

            # total_cost_3 = await sync_to_async(lambda: query_user.aggregate(Sum('budget_planned')))()
            # total_cost_3 = total_cost_3['budget_planned__sum'] or 0
            # total_cost_4 = await sync_to_async(lambda: query_user.aggregate(Sum('off_budget_planned')))()
            # total_cost_4 = total_cost_4['off_budget_planned__sum'] or 0
            # total_cost_5 = await sync_to_async(lambda: query_user.aggregate(Sum('budget_bargaining')))()
            # total_cost_5 = total_cost_5['budget_bargaining__sum'] or 0
            # total_cost_6 = await sync_to_async(lambda: query_user.aggregate(Sum('off_budget_bargaining')))()
            # total_cost_6 = total_cost_6['off_budget_bargaining__sum'] or 0
            # total_cost_7 = await sync_to_async(lambda: query_user.aggregate(Sum('budget_concluded')))()
            # total_cost_7 = total_cost_7['budget_concluded__sum'] or 0
            # total_cost_8 = await sync_to_async(lambda: query_user.aggregate(Sum('off_budget_concluded')))()
            # total_cost_8 = total_cost_8['off_budget_concluded__sum'] or 0
            # total_cost_9 = await sync_to_async(lambda: query_user.aggregate(Sum('budget_completed')))()
            # total_cost_9 = total_cost_9['budget_completed__sum'] or 0
            # total_cost_10 = await sync_to_async(lambda: query_user.aggregate(Sum('off_budget_completed')))()
            # total_cost_10 = total_cost_10['off_budget_completed__sum'] or 0

            # if total_cost_1 < (total_cost_3 or total_cost_5 or total_cost_7 or total_cost_9):
            #     await sync_to_async(new_service.delete)()
            #     await sync_to_async(messages.error)(request, 'Запрещено вносить новую строку, если после ее ввода сумма контактов по соответствующему КЦСР, КОСГУ и ДопФК превысит значение поля «Лимиты»')

            #     return render(request, 'add.html', context_data)

            # if total_cost_2 < (total_cost_4 or total_cost_5 or total_cost_8 or total_cost_10):
            #     await sync_to_async(new_service.delete)()
            #     await sync_to_async(messages.error)(request, 'Запрещено вносить новую строку, если после ее ввода сумма контактов по соответствующему КЦСР, КОСГУ и ДопФК превысит значение поля «Лимиты»')

            #     return render(request, 'add.html', context_data)

            # from django.db.models import Q

            # Services_2016100000_ = await sync_to_async(list)(Services.objects.filter(
            #     Q(KOSGU=context_data['KOSGU']) & Q(DopFC=context_data['DopFC']) & Q(KTSSR='2016100000')
            # ))

            # execution_contract_fact_sum_2016100000 = 0
            # for service in Services_2016100000_:
            #     execution_contract_fact_sum_2016100000 += await clean_number(service.execution_contract_fact if service.execution_contract_fact not in [None, 'None', ''] else 0)

            # Services_2016100092_ = await sync_to_async(list)(Services.objects.filter(
            #     Q(KOSGU=context_data['KOSGU']) & Q(DopFC=context_data['DopFC']) & Q(KTSSR='2016100092')
            # ))

            # execution_contract_fact_sum_2016100092 = 0
            # for service in Services_2016100092_:
            #     execution_contract_fact_sum_2016100092 += await clean_number(service.execution_contract_fact if service.execution_contract_fact not in [None, 'None', ''] else 0)

            # Services_planned_2016100000_ = await sync_to_async(list)(Services.objects.filter(
            #     Q(KOSGU=context_data['KOSGU']) & Q(DopFC=context_data['DopFC']) & Q(KTSSR='2016100000') & Q(status='Запланировано')
            # ))

            # contract_price_sum_planned_2016100000 = 0
            # for service in Services_planned_2016100000_:
            #     contract_price_sum_planned_2016100000 += await clean_number(service.contract_price if service.contract_price not in [None, 'None', ''] else 0)

            # Services_off_planned_2016100092_ = await sync_to_async(list)(Services.objects.filter(
            #     Q(KOSGU=context_data['KOSGU']) & Q(DopFC=context_data['DopFC']) & Q(KTSSR='2016100092') & Q(status='Запланировано')
            # ))

            # contract_price_sum_off_planned_2016100092 = 0
            # for service in Services_off_planned_2016100092_:
            #     contract_price_sum_off_planned_2016100092 += await clean_number(service.contract_price if service.contract_price not in [None, 'None', ''] else 0)

            # Services_bargaining_2016100000_ = await sync_to_async(list)(Services.objects.filter(
            #     Q(KOSGU=context_data['KOSGU']) & Q(DopFC=context_data['DopFC']) & Q(KTSSR='2016100000') & Q(status='В торгах')
            # ))

            # contract_price_sum_bargaining_2016100000 = 0
            # for service in Services_bargaining_2016100000_:
            #     contract_price_sum_bargaining_2016100000 += await clean_number(service.contract_price if service.contract_price not in [None, 'None', ''] else 0)

            # Services_off_bargaining_2016100092_ = await sync_to_async(list)(Services.objects.filter(
            #     Q(KOSGU=context_data['KOSGU']) & Q(DopFC=context_data['DopFC']) & Q(KTSSR='2016100092') & Q(status='В торгах')
            # ))

            # contract_price_sum_off_bargaining_2016100092 = 0
            # for service in Services_off_bargaining_2016100092_:
            #     contract_price_sum_off_bargaining_2016100092 += await clean_number(service.contract_price if service.contract_price not in [None, 'None', ''] else 0)

            # Services_concluded_2016100000_ = await sync_to_async(list)(Services.objects.filter(
            #     Q(KOSGU=context_data['KOSGU']) & Q(DopFC=context_data['DopFC']) & Q(KTSSR='2016100000') & Q(status='Заключено')
            # ))

            # contract_price_sum_concluded_2016100000 = 0
            # for service in Services_concluded_2016100000_:
            #     contract_price_sum_concluded_2016100000 += await clean_number(service.contract_price if service.contract_price not in [None, 'None', ''] else 0)

            # Services_off_concluded_2016100092_ = await sync_to_async(list)(Services.objects.filter(
            #     Q(KOSGU=context_data['KOSGU']) & Q(DopFC=context_data['DopFC']) & Q(KTSSR='2016100092') & Q(status='Заключено')
            # ))

            # contract_price_sum_off_concluded_2016100092 = 0
            # for service in Services_off_concluded_2016100092_:
            #     contract_price_sum_off_concluded_2016100092 += await clean_number(service.contract_price if service.contract_price not in [None, 'None', ''] else 0)

            # Services_completed_2016100000_ = await sync_to_async(list)(Services.objects.filter(
            #     Q(KOSGU=context_data['KOSGU']) & Q(DopFC=context_data['DopFC']) & Q(KTSSR='2016100000') & Q(status='Исполнено')
            # ))

            # contract_price_sum_completed_2016100000 = 0
            # for service in Services_completed_2016100000_:
            #     contract_price_sum_completed_2016100000 += await clean_number(service.contract_price if service.contract_price not in [None, 'None', ''] else 0)

            # Services_off_completed_2016100092_ = await sync_to_async(list)(Services.objects.filter(
            #     Q(KOSGU=context_data['KOSGU']) & Q(DopFC=context_data['DopFC']) & Q(KTSSR='2016100092') & Q(status='Исполнено')
            # ))

            # contract_price_sum_off_completed_2016100092 = 0
            # for service in Services_off_completed_2016100092_:
            #     contract_price_sum_off_completed_2016100092 += await clean_number(service.contract_price if service.contract_price not in [None, 'None', ''] else 0)

            # Services_way_ = await sync_to_async(list)(Services.objects.filter(
            #     Q(KOSGU=context_data['KOSGU']) & Q(DopFC=context_data['DopFC']) & Q(KTSSR=context_data['KTSSR']) & Q(status=context_data['status']) & Q(way='п.4 ч.1 ст.93')
            # ))
            # contract_price_sum_way = 0
            # execution_contract_fact_sum_way = 0
            # for service in Services_way_:
            #     contract_price_sum_way += await clean_number(service.contract_price if service.contract_price not in [None, 'None', ''] else 0)
            #     execution_contract_fact_sum_way += await clean_number(service.execution_contract_fact if service.execution_contract_fact not in [None, 'None', ''] else 0)

            # try:
            #     from django.db.models import Q

            #     ServicesVault_ = await sync_to_async(ServicesVault.objects.get)(
            #         Q(KOSGU=context_data['KOSGU']) & Q(DopFC=context_data['DopFC'])
            #     )
            # except:
            #     await sync_to_async(messages.error)(request, 'Нет сопоставления КОСГУ с ДопФК')

            #     return render(request, 'add.html', context_data)

            # ServicesVault_.off_budget_planned = contract_price_sum_off_planned_2016100092

            # ServicesVault_.budget_planned = contract_price_sum_planned_2016100000

            # ServicesVault_.off_budget_bargaining = contract_price_sum_off_bargaining_2016100092

            # ServicesVault_.budget_bargaining = contract_price_sum_bargaining_2016100000

            # ServicesVault_.off_budget_concluded = contract_price_sum_off_concluded_2016100092

            # ServicesVault_.budget_concluded = contract_price_sum_concluded_2016100000

            # ServicesVault_.off_budget_completed = contract_price_sum_off_completed_2016100092

            # ServicesVault_.budget_completed = contract_price_sum_completed_2016100000

            # if context_data['KTSSR'] == '2016100092':
            #     ServicesVault_.off_budget_execution = execution_contract_fact_sum_2016100092
            # elif context_data['KTSSR'] == '2016100000':
            #     ServicesVault_.budget_execution = execution_contract_fact_sum_2016100000

            # await sync_to_async(ServicesVault_.save)()

            # try:
            #     from django.db.models import Q

            #     ServicesVault_ = await sync_to_async(ServicesVault.objects.get)(
            #         Q(KOSGU=context_data['KOSGU']) & Q(DopFC=context_data['DopFC'])
            #     )
            # except:
            #     await sync_to_async(messages.error)(request, 'Нет сопоставления КОСГУ с ДопФК')

            #     return render(request, 'edit.html', context_data)

            # # Создаем список месяцев
            # budget = [
            #     ServicesVault_.budget_limit if ServicesVault_.budget_limit not in [None, 'None', ''] else 0,
            #     ServicesVault_.budget_bargaining if ServicesVault_.budget_bargaining not in [None, 'None', ''] else 0,
            #     ServicesVault_.budget_concluded if ServicesVault_.budget_concluded not in [None, 'None', ''] else 0,
            #     ServicesVault_.budget_completed if ServicesVault_.budget_completed not in [None, 'None', ''] else 0
            # ]

            # # Асинхронно обрабатываем все месяцы
            # cleaned_numbers = await asyncio.gather(*(clean_number(number) for number in budget))

            # # Суммируем результат
            # ServicesVault_.budget_remainder = cleaned_numbers[0] - sum(cleaned_numbers[1:])

            # # Создаем список месяцев
            # off_budget = [
            #     ServicesVault_.off_budget_limit if ServicesVault_.off_budget_limit not in [None, 'None', ''] else 0,
            #     ServicesVault_.off_budget_bargaining if ServicesVault_.off_budget_bargaining not in [None, 'None', ''] else 0,
            #     ServicesVault_.off_budget_concluded if ServicesVault_.off_budget_concluded not in [None, 'None', ''] else 0,
            #     ServicesVault_.off_budget_completed if ServicesVault_.off_budget_completed not in [None, 'None', ''] else 0
            # ]

            # # Асинхронно обрабатываем все месяцы
            # cleaned_numbers = await asyncio.gather(*(clean_number(number) for number in off_budget))

            # # Суммируем результат
            # ServicesVault_.off_budget_remainder = cleaned_numbers[0] - sum(cleaned_numbers[1:])

            # ServicesVault_.budget_plans = await clean_number(ServicesVault_.budget_remainder if ServicesVault_.budget_remainder not in [None, 'None', ''] else 0) - await clean_number(ServicesVault_.budget_planned if ServicesVault_.budget_planned not in [None, 'None', ''] else 0)
            # ServicesVault_.off_budget_plans = await clean_number(ServicesVault_.off_budget_remainder if ServicesVault_.off_budget_remainder not in [None, 'None', ''] else 0) - await clean_number(ServicesVault_.off_budget_planned if ServicesVault_.off_budget_planned not in [None, 'None', ''] else 0)

            # if any(x < 0 for x in [await clean_number(ServicesVault_.budget_remainder), await clean_number(ServicesVault_.off_budget_remainder), await clean_number(ServicesVault_.budget_plans), await clean_number(ServicesVault_.off_budget_plans)]):
            #     ServicesVault_.color = '#ffebeb'
            # else:
            #     ServicesVault_.color = ''

            # await sync_to_async(ServicesVault_.save)()

            # try:
            #     from django.db.models import Q

            #     ServicesTwo_ = await sync_to_async(ServicesTwo.objects.get)(
            #         Q(KOSGU=context_data['KOSGU']) & Q(DopFC=context_data['DopFC'])
            #     )

            #     ServicesVault_ = await sync_to_async(ServicesVault.objects.get)(
            #         Q(KOSGU=context_data['KOSGU']) & Q(DopFC=context_data['DopFC'])
            #     )

            #     if context_data['status'] == 'Заключено' and context_data['KTSSR'] == '2016100092':
            #         ServicesTwo_.off_budget_concluded = contract_price_sum_way
            #         ServicesTwo_.off_budget_remainder = await clean_number(ServicesTwo_.off_budget_planned) - await clean_number(contract_price_sum_way)
            #     elif context_data['status'] == 'Заключено' and context_data['KTSSR'] == '2016100000':
            #         ServicesTwo_.budget_concluded = contract_price_sum_way
            #         ServicesTwo_.budget_remainder = await clean_number(ServicesTwo_.budget_planned) - await clean_number(contract_price_sum_way)

            #     if any(x < 0 for x in [await clean_number(ServicesVault_.budget_remainder), await clean_number(ServicesVault_.off_budget_remainder), await clean_number(ServicesVault_.budget_plans), await clean_number(ServicesVault_.off_budget_plans)]):
            #         ServicesTwo_.color = '#ffebeb'
            #     else:
            #         ServicesTwo_.color = ''

            #     await sync_to_async(ServicesTwo_.save)()

            # except Exception as e:
            #     # Вывод подробной информации об ошибке
            #     print(f"Поймано исключение: {type(e).__name__}")
            #     print(f"Сообщение об ошибке: {str(e)}")
            #     import traceback
            #     print("Трассировка стека (stack trace):")
            #     traceback.print_exc()

            # await sync_to_async(messages.success)(request, 'Данные успешно добавлены!')

            # # Перенаправление с несколькими параметрами
            # return redirect(f"/?{urlencode(context_data)}")

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

            # # Найдите запись по ID и обновите цвет
            # service = await sync_to_async(Services.objects.get)(id=row_id)

            # KOSGU = service.KOSGU

            # DopFC = service.DopFC

            # KTSSR = service.KTSSR

            # status = service.status

            # # Удаление записи
            # await sync_to_async(service.delete)()

            # try:
            #     from django.db.models import Q

            #     Services_ = await sync_to_async(list)(Services.objects.filter(
            #         Q(KOSGU=KOSGU) & Q(DopFC=DopFC) & Q(KTSSR=KTSSR) & Q(status=status)
            #     ))
            #     contract_price_sum = 0
            #     execution_contract_fact_sum = 0
            #     for service in Services_:
            #         contract_price_sum += await clean_number(service.contract_price if service.contract_price not in [None, 'None', ''] else 0)
            #         execution_contract_fact_sum += await clean_number(service.execution_contract_fact if service.execution_contract_fact not in [None, 'None', ''] else 0)

            #     Services_way_ = await sync_to_async(list)(Services.objects.filter(
            #         Q(KOSGU=KOSGU) & Q(DopFC=DopFC) & Q(KTSSR=KTSSR) & Q(status=status) & Q(way='п.4 ч.1 ст.93')
            #     ))
            #     contract_price_sum_way = 0
            #     execution_contract_fact_sum_way = 0
            #     for service in Services_way_:
            #         contract_price_sum_way += await clean_number(service.contract_price if service.contract_price not in [None, 'None', ''] else 0)
            #         execution_contract_fact_sum_way += await clean_number(service.execution_contract_fact if service.execution_contract_fact not in [None, 'None', ''] else 0)

            #     from django.db.models import Q

            #     ServicesVault_ = await sync_to_async(ServicesVault.objects.get)(
            #         Q(KOSGU=KOSGU) & Q(DopFC=DopFC)
            #     )

            #     if status == 'В торгах' and KTSSR == '2016100092':
            #         ServicesVault_.off_budget_bargaining = contract_price_sum
            #     elif status == 'В торгах' and KTSSR == '2016100000':
            #         ServicesVault_.budget_bargaining = contract_price_sum
            #     elif status == 'Запланировано' and KTSSR == '2016100092':
            #         ServicesVault_.off_budget_planned = contract_price_sum
            #     elif status == 'Запланировано' and KTSSR == '2016100000':
            #         ServicesVault_.budget_planned = contract_price_sum
            #     elif status == 'Заключено' and KTSSR == '2016100092':
            #         ServicesVault_.off_budget_concluded = contract_price_sum
            #     elif status == 'Заключено' and KTSSR == '2016100000':
            #         ServicesVault_.budget_concluded = contract_price_sum
            #     elif status == 'Исполнено' and KTSSR == '2016100092':
            #         ServicesVault_.off_budget_completed = contract_price_sum
            #     elif status == 'Исполнено' and KTSSR == '2016100000':
            #         ServicesVault_.budget_completed = contract_price_sum

            #     if KTSSR == '2016100092':
            #         ServicesVault_.off_budget_execution = execution_contract_fact_sum
            #     elif KTSSR == '2016100000':
            #         ServicesVault_.budget_execution = execution_contract_fact_sum

            #     # Создаем список месяцев
            #     budget = [
            #         ServicesVault_.budget_limit if ServicesVault_.budget_limit not in [None, 'None', ''] else 0,
            #         ServicesVault_.budget_bargaining if ServicesVault_.budget_bargaining not in [None, 'None', ''] else 0,
            #         ServicesVault_.budget_concluded if ServicesVault_.budget_concluded not in [None, 'None', ''] else 0,
            #         ServicesVault_.budget_completed if ServicesVault_.budget_completed not in [None, 'None', ''] else 0
            #     ]

            #     # Асинхронно обрабатываем все месяцы
            #     cleaned_numbers = await asyncio.gather(*(clean_number(number) for number in budget))

            #     # Суммируем результат
            #     ServicesVault_.budget_remainder = cleaned_numbers[0] - sum(cleaned_numbers[1:])

            #     # Создаем список месяцев
            #     off_budget = [
            #         ServicesVault_.off_budget_limit if ServicesVault_.off_budget_limit not in [None, 'None', ''] else 0,
            #         ServicesVault_.off_budget_bargaining if ServicesVault_.off_budget_bargaining not in [None, 'None', ''] else 0,
            #         ServicesVault_.off_budget_concluded if ServicesVault_.off_budget_concluded not in [None, 'None', ''] else 0,
            #         ServicesVault_.off_budget_completed if ServicesVault_.off_budget_completed not in [None, 'None', ''] else 0
            #     ]

            #     # Асинхронно обрабатываем все месяцы
            #     cleaned_numbers = await asyncio.gather(*(clean_number(number) for number in off_budget))

            #     # Суммируем результат
            #     ServicesVault_.off_budget_remainder = cleaned_numbers[0] - sum(cleaned_numbers[1:])

            #     ServicesVault_.budget_plans = await clean_number(ServicesVault_.budget_remainder if ServicesVault_.budget_remainder not in [None, 'None', ''] else 0) - await clean_number(ServicesVault_.budget_planned if ServicesVault_.budget_planned not in [None, 'None', ''] else 0)
            #     ServicesVault_.off_budget_plans = await clean_number(ServicesVault_.off_budget_remainder if ServicesVault_.off_budget_remainder not in [None, 'None', ''] else 0) - await clean_number(ServicesVault_.off_budget_planned if ServicesVault_.off_budget_planned not in [None, 'None', ''] else 0)

            #     if any(x < 0 for x in [await clean_number(ServicesVault_.budget_remainder), await clean_number(ServicesVault_.off_budget_remainder), await clean_number(ServicesVault_.budget_plans), await clean_number(ServicesVault_.off_budget_plans)]):
            #         ServicesVault_.color = '#ffebeb'
            #     else:
            #         ServicesVault_.color = ''

            #     await sync_to_async(ServicesVault_.save)()

            # except Exception as e:
            #     # Вывод подробной информации об ошибке
            #     print(f"Поймано исключение: {type(e).__name__}")
            #     print(f"Сообщение об ошибке: {str(e)}")
            #     import traceback
            #     print("Трассировка стека (stack trace):")
            #     traceback.print_exc()

            # try:
            #     from django.db.models import Q

            #     ServicesTwo_ = await sync_to_async(ServicesTwo.objects.get)(
            #         Q(KOSGU=KOSGU) & Q(DopFC=DopFC)
            #     )

            #     ServicesVault_ = await sync_to_async(ServicesVault.objects.get)(
            #         Q(KOSGU=KOSGU) & Q(DopFC=DopFC)
            #     )

            #     if status == 'Заключено' and KTSSR == '2016100092':
            #         ServicesTwo_.off_budget_concluded = contract_price_sum_way
            #         ServicesTwo_.off_budget_remainder = await clean_number(ServicesTwo_.off_budget_planned) - await clean_number(contract_price_sum_way)
            #     elif status == 'Заключено' and KTSSR == '2016100000':
            #         ServicesTwo_.budget_concluded = contract_price_sum_way
            #         ServicesTwo_.budget_remainder = await clean_number(ServicesTwo_.budget_planned) - await clean_number(contract_price_sum_way)

            #     if any(x < 0 for x in [await clean_number(ServicesVault_.budget_remainder), await clean_number(ServicesVault_.off_budget_remainder), await clean_number(ServicesVault_.budget_plans), await clean_number(ServicesVault_.off_budget_plans)]):
            #         ServicesTwo_.color = '#ffebeb'
            #     else:
            #         ServicesTwo_.color = ''

            #     await sync_to_async(ServicesTwo_.save)()

            # except Exception as e:
            #     # Вывод подробной информации об ошибке
            #     print(f"Поймано исключение: {type(e).__name__}")
            #     print(f"Сообщение об ошибке: {str(e)}")
            #     import traceback
            #     print("Трассировка стека (stack trace):")
            #     traceback.print_exc()

            # # Сообщение об успешном удалении
            # await sync_to_async(messages.success)(request, 'Данные успешно удалены!')

            # Перенаправление на главную страницу
            return redirect('data_table_view')
        except Services.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Service not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON.'}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)