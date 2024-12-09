from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Services, ServicesVault, ServicesTwo
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render
import re
from django.db.models import Sum
from asgiref.sync import sync_to_async

# async def skeleton(request, user, contract_date, end_date, keyword_one, keyword_two, selected_column_one, selected_column_two, page):
#     contract_date = None if contract_date == 'None' else contract_date
#     end_date = None if end_date == 'None' else end_date
#     keyword_one = None if keyword_one == 'None' else keyword_one
#     keyword_two = None if keyword_two == 'None' else keyword_two
#     selected_column_one = None if selected_column_one == 'None' else selected_column_one
#     selected_column_two = None if selected_column_two == 'None' else selected_column_two

#     per_page = 20

#     # Регулярные выражения для форматов дат
#     pattern_dd_mm_yyyy = r'\b\d{2}\.\d{2}\.\d{4}\b'
#     pattern_yyyy_mm_dd = r'\b\d{4}-\d{2}-\d{2}\b'

#     # Получаем все уникальные значения year и date_number_no_one
#     # all_years = await sync_to_async(Services.objects.values('year').distinct())
#     all_years = await sync_to_async(lambda: list(Services.objects.values('contract_date').distinct()))()
#     # all_date_number_no_one = await sync_to_async(Services.objects.values('date_number_no_one').distinct())
#     all_end_date = await sync_to_async(lambda: list(Services.objects.values('end_date').distinct()))()

#     # Сбор уникальных годов из year
#     service_years = set()
#     empty_found_contract_date = False
#     for year_value in all_years:
#         year_str = year_value['contract_date']
#         if not year_str:
#             empty_found_contract_date = True
#         matches_dd_mm_yyyy = re.findall(pattern_dd_mm_yyyy, year_str)
#         matches_yyyy_mm_dd = re.findall(pattern_yyyy_mm_dd, year_str)
#         service_years.update([date_str[-4:] for date_str in matches_dd_mm_yyyy])
#         service_years.update([date_str[:4] for date_str in matches_yyyy_mm_dd])

#     service_years = sorted({str(int(contract_date)) for contract_date in service_years if contract_date.isdigit()})
#     if empty_found_contract_date:
#         service_years.insert(0, None)

#     # Сбор уникальных годов из date_number_no_one
#     service_end_date = set()
#     empty_found_end_date = False
#     for date_value in all_end_date:
#         date_str = date_value['end_date']
#         if not date_str:
#             empty_found_end_date = True
#         matches_dd_mm_yyyy = re.findall(pattern_dd_mm_yyyy, date_str)
#         matches_yyyy_mm_dd = re.findall(pattern_yyyy_mm_dd, date_str)
#         service_end_date.update([date_str[-4:] for date_str in matches_dd_mm_yyyy])
#         service_end_date.update([date_str[:4] for date_str in matches_yyyy_mm_dd])

#     service_end_date = sorted({str(int(end_date)) for end_date in service_end_date if end_date.isdigit()})
#     if empty_found_end_date:
#         service_end_date.insert(0, None)

#     # Построение запроса
#     # query = await sync_to_async(Services.objects.all)()
#     query = await sync_to_async(lambda: Services.objects.all())()

#     if contract_date == 'No':
#         contract_date = None
#     if end_date == 'No':
#         end_date = None

#     if contract_date == 'None' and end_date == 'None':
#         query = await sync_to_async(query.exclude)(Q(contract_date__regex=pattern_dd_mm_yyyy) | Q(contract_date__regex=pattern_yyyy_mm_dd) |
#                             Q(end_date__regex=pattern_dd_mm_yyyy) | Q(end_date__regex=pattern_yyyy_mm_dd))
#     elif contract_date == 'None' and end_date:
#         query = await sync_to_async(query.exclude)(Q(contract_date__regex=pattern_dd_mm_yyyy) | Q(contract_date__regex=pattern_yyyy_mm_dd))
#         query = await sync_to_async(query.filter)(end_date__icontains=end_date)
#     elif contract_date == 'None' and not end_date:
#         query = await sync_to_async(query.exclude)(Q(contract_date__regex=pattern_dd_mm_yyyy) | Q(contract_date__regex=pattern_yyyy_mm_dd))
#     elif contract_date and end_date == 'None':
#         query = await sync_to_async(query.exclude)(Q(end_date__regex=pattern_dd_mm_yyyy) | Q(end_date__regex=pattern_yyyy_mm_dd))
#         query = await sync_to_async(query.filter)(contract_date__icontains=contract_date)
#     elif not contract_date and end_date == 'None':
#         query = await sync_to_async(query.exclude)(Q(end_date__regex=pattern_dd_mm_yyyy) | Q(end_date__regex=pattern_yyyy_mm_dd))
#     elif contract_date and end_date:
#         query = await sync_to_async(query.filter)(Q(contract_date__icontains=contract_date) | Q(end_date__icontains=end_date))
#     elif contract_date and not end_date:
#         query = await sync_to_async(query.filter)(contract_date__icontains=contract_date)
#     elif not contract_date and end_date:
#         query = await sync_to_async(query.filter)(end_date__icontains=end_date)

#     if keyword_one:
#         if selected_column_one and hasattr(Services, selected_column_one):
#             query = await sync_to_async(query.filter)(**{selected_column_one + '__icontains': keyword_one})
#         else:
#             filters = Q()
#             for field in await sync_to_async(Services._meta.get_fields)():
#                 filters |= Q(**{field.name + '__icontains': keyword_one})
#             query = await sync_to_async(query.filter)(filters)

#     if keyword_two:
#         if selected_column_two and hasattr(Services, selected_column_two):
#             query = await sync_to_async(query.filter)(**{selected_column_two + '__icontains': keyword_two})
#         else:
#             filters = Q()
#             for field in await sync_to_async(Services._meta.get_fields)():
#                 filters |= Q(**{field.name + '__icontains': keyword_two})
#             query = await sync_to_async(query.filter)(filters)

#     # Сортировка
#     # query = query.order_by('id_id', 'contract_date')

#     from django.db.models import IntegerField, DateField
#     from django.db.models.functions import Cast

#     # Преобразование id_id в целое число и contract_date в дату перед сортировкой
#     query = query.annotate(
#         id_id_int=Cast('id_id', IntegerField()),
#         contract_date_date=Cast('contract_date', DateField())
#     ).order_by('id_id_int', 'contract_date_date')

#     # # Логика подсчета стоимости
#     # if contract_date == 'None' and end_date == 'None':
#     #     total_cost_1 = await sync_to_async(query.exclude)(Q(year__regex=pattern_dd_mm_yyyy) | Q(year__regex=pattern_yyyy_mm_dd) |
#     #                                 Q(date_number_no_one__regex=pattern_dd_mm_yyyy) | Q(date_number_no_one__regex=pattern_yyyy_mm_dd)).aggregate(Sum('cost'))['cost__sum'] or 0
#     #     total_cost_2 = await sync_to_async(query.exclude)(Q(year__regex=pattern_dd_mm_yyyy) | Q(year__regex=pattern_yyyy_mm_dd) |
#     #                                 Q(date_number_no_one__regex=pattern_dd_mm_yyyy) | Q(date_number_no_one__regex=pattern_yyyy_mm_dd)).aggregate(Sum('certificate'))['certificate__sum'] or 0
#     #     total_cost_3 = await sync_to_async(query.exclude)(Q(year__regex=pattern_dd_mm_yyyy) | Q(year__regex=pattern_yyyy_mm_dd) |
#     #                                 Q(date_number_no_one__regex=pattern_dd_mm_yyyy) | Q(date_number_no_one__regex=pattern_yyyy_mm_dd)).aggregate(Sum('certificate_no'))['certificate_no__sum'] or 0
#     # elif contract_date and end_date:
#     #     total_cost_1 = await sync_to_async(query.filter)(Q(year__icontains=contract_date) | Q(date_number_no_one__icontains=contract_date)).aggregate(Sum('cost'))['cost__sum'] or 0
#     #     total_cost_2 = await sync_to_async(query.filter)(Q(year__icontains=contract_date) | Q(date_number_no_one__icontains=contract_date)).aggregate(Sum('certificate'))['certificate__sum'] or 0
#     #     total_cost_3 = await sync_to_async(query.filter)(Q(year__icontains=contract_date) | Q(date_number_no_one__icontains=contract_date)).aggregate(Sum('certificate_no'))['certificate_no__sum'] or 0
#     # elif contract_date == 'None' and end_date != 'None':
#     #     total_cost_1 = await sync_to_async(query.exclude)(Q(year__regex=pattern_dd_mm_yyyy) | Q(year__regex=pattern_yyyy_mm_dd)).aggregate(Sum('cost'))['cost__sum'] or 0
#     #     total_cost_2 = await sync_to_async(query.exclude)(Q(year__regex=pattern_dd_mm_yyyy) | Q(year__regex=pattern_yyyy_mm_dd)).aggregate(Sum('certificate'))['certificate__sum'] or 0
#     #     total_cost_3 = await sync_to_async(query.exclude)(Q(year__regex=pattern_dd_mm_yyyy) | Q(year__regex=pattern_yyyy_mm_dd)).aggregate(Sum('certificate_no'))['certificate_no__sum'] or 0
#     # elif contract_date and not end_date:
#     #     total_cost_1 = await sync_to_async(query.filter)(Q(year__icontains=contract_date)).aggregate(Sum('cost'))['cost__sum'] or 0
#     #     total_cost_2 = await sync_to_async(query.filter)(Q(year__icontains=contract_date)).aggregate(Sum('certificate'))['certificate__sum'] or 0
#     #     total_cost_3 = await sync_to_async(query.filter)(Q(year__icontains=contract_date)).aggregate(Sum('certificate_no'))['certificate_no__sum'] or 0
#     # elif contract_date != 'None' and end_date == 'None':
#     #     total_cost_1 = await sync_to_async(query.exclude)(Q(date_number_no_one__regex=pattern_dd_mm_yyyy) | Q(date_number_no_one__regex=pattern_yyyy_mm_dd)).aggregate(Sum('cost'))['cost__sum'] or 0
#     #     total_cost_2 = await sync_to_async(query.exclude)(Q(date_number_no_one__regex=pattern_dd_mm_yyyy) | Q(date_number_no_one__regex=pattern_yyyy_mm_dd)).aggregate(Sum('certificate'))['certificate__sum'] or 0
#     #     total_cost_3 = await sync_to_async(query.exclude)(Q(date_number_no_one__regex=pattern_dd_mm_yyyy) | Q(date_number_no_one__regex=pattern_yyyy_mm_dd)).aggregate(Sum('certificate_no'))['certificate_no__sum'] or 0
#     # elif not contract_date and end_date:
#     #     total_cost_1 = await sync_to_async(query.filter)(Q(date_number_no_one__icontains=end_date)).aggregate(Sum('cost'))['cost__sum'] or 0
#     #     total_cost_2 = await sync_to_async(query.filter)(Q(date_number_no_one__icontains=end_date)).aggregate(Sum('certificate'))['certificate__sum'] or 0
#     #     total_cost_3 = await sync_to_async(query.filter)(Q(date_number_no_one__icontains=end_date)).aggregate(Sum('certificate_no'))['certificate_no__sum'] or 0
#     # else:
#     #     # total_cost_1 = query.aggregate(Sum('cost'))['cost__sum'] or 0
#     #     total_cost_1 = await sync_to_async(lambda: query.aggregate(Sum('cost')))()
#     #     total_cost_1 = total_cost_1['cost__sum'] or 0

#     #     # total_cost_2 = query.aggregate(Sum('certificate'))['certificate__sum'] or 0
#     #     total_cost_2 = await sync_to_async(lambda: query.aggregate(Sum('certificate')))()
#     #     total_cost_2 = total_cost_2['certificate__sum'] or 0

#     #     # total_cost_3 = query.aggregate(Sum('certificate_no'))['certificate_no__sum'] or 0
#     #     total_cost_3 = await sync_to_async(lambda: query.aggregate(Sum('certificate_no')))()
#     #     total_cost_3 = total_cost_3['certificate_no__sum'] or 0

#     # Пагинация
#     paginator = Paginator(query, per_page)
#     services = await sync_to_async(paginator.get_page)(page)

#     # Получаем общее количество страниц
#     total_pages = paginator.num_pages

#     # Определяем максимальное количество кнопок для навигации
#     max_page_buttons = 5
#     start_page = max(1, page - max_page_buttons // 2)
#     end_page = min(total_pages, page + max_page_buttons // 2)

#     if end_page - start_page < max_page_buttons - 1:
#         if start_page > 1:
#             end_page = min(total_pages, end_page + (max_page_buttons - (end_page - start_page)))
#         else:
#             start_page = max(1, end_page - (max_page_buttons - (end_page - start_page)))

#     pages = range(start_page, end_page + 1)  # Создаем диапазон страниц

#     # Подготовка контекста для шаблона
#     context = {
#         'data': services,
#         'user': user,
#         'pages': pages,
#         # 'total_cost_1': total_cost_1,
#         # 'total_cost_2': total_cost_2,
#         # 'total_cost_3': total_cost_3,
#         'selected_contract_date': contract_date,
#         'selected_end_date': end_date,
#         'selected_column_one': selected_column_one,
#         'selected_column_two': selected_column_two,
#         'keyword_one': keyword_one,
#         'keyword_two': keyword_two,
#         'page': page,
#         'total_pages': total_pages,
#         'start_page': start_page,
#         'end_page': end_page,
#         'service_years': service_years,
#         'service_end_date': service_end_date
#     }

#     return await sync_to_async(render)(request, 'data_table.html', context)

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
    # all_years = await sync_to_async(Services.objects.values('year').distinct())
    all_years = await sync_to_async(lambda: list(Services.objects.values('contract_date').distinct()))()
    # all_date_number_no_one = await sync_to_async(Services.objects.values('date_number_no_one').distinct())
    all_end_date = await sync_to_async(lambda: list(Services.objects.values('end_date').distinct()))()

    all_KOSGU_user = await sync_to_async(lambda: list(ServicesVault.objects.values('KOSGU').distinct()))()

    all_KOSGU_user_two = await sync_to_async(lambda: list(ServicesTwo.objects.values('KOSGU').distinct()))()

    # Сбор уникальных all_KOSGU_user
    service_KOSGU_user = set()
    empty_found_KOSGU = False
    for year_value in all_KOSGU_user:
        year_str = year_value.get('KOSGU', None)
        if not year_str:
            empty_found_KOSGU = True
            continue # Пропустить итерацию, если year_str пустой или None
        matches_dd_mm_yyyy = re.findall(pattern_dd_mm_yyyy, year_str)
        matches_yyyy_mm_dd = re.findall(pattern_yyyy_mm_dd, year_str)
        service_KOSGU_user.update([date_str[-4:] for date_str in matches_dd_mm_yyyy])
        service_KOSGU_user.update([date_str[:4] for date_str in matches_yyyy_mm_dd])

    service_KOSGU_user = sorted({str(int(KOSGU)) for KOSGU in service_KOSGU_user if KOSGU.isdigit()})
    if empty_found_KOSGU:
        service_KOSGU_user.insert(0, None)

    # Сбор уникальных all_KOSGU_user_two
    service_KOSGU_user_two = set()
    empty_found_KOSGU = False
    for year_value in all_KOSGU_user_two:
        year_str = year_value.get('KOSGU', None)
        if not year_str:
            empty_found_KOSGU = True
            continue # Пропустить итерацию, если year_str пустой или None
        matches_dd_mm_yyyy = re.findall(pattern_dd_mm_yyyy, year_str)
        matches_yyyy_mm_dd = re.findall(pattern_yyyy_mm_dd, year_str)
        service_KOSGU_user_two.update([date_str[-4:] for date_str in matches_dd_mm_yyyy])
        service_KOSGU_user_two.update([date_str[:4] for date_str in matches_yyyy_mm_dd])

    service_KOSGU_user_two = sorted({str(int(KOSGU)) for KOSGU in service_KOSGU_user_two if KOSGU.isdigit()})
    if empty_found_KOSGU:
        service_KOSGU_user_two.insert(0, None)

    # Сбор уникальных годов из year
    service_years = set()
    empty_found_contract_date = False
    for year_value in all_years:
        year_str = year_value.get('contract_date', None)
        if not year_str:
            empty_found_contract_date = True
            continue
        matches_dd_mm_yyyy = re.findall(pattern_dd_mm_yyyy, year_str)
        matches_yyyy_mm_dd = re.findall(pattern_yyyy_mm_dd, year_str)
        service_years.update([date_str[-4:] for date_str in matches_dd_mm_yyyy])
        service_years.update([date_str[:4] for date_str in matches_yyyy_mm_dd])

    service_years = sorted({str(int(contract_date)) for contract_date in service_years if contract_date.isdigit()})
    if empty_found_contract_date:
        service_years.insert(0, None)

    # Сбор уникальных годов из date_number_no_one
    service_end_date = set()
    empty_found_end_date = False
    for date_value in all_end_date:
        date_str = date_value.get('end_date', None)
        if not date_str:
            empty_found_end_date = True
            continue
        matches_dd_mm_yyyy = re.findall(pattern_dd_mm_yyyy, date_str)
        matches_yyyy_mm_dd = re.findall(pattern_yyyy_mm_dd, date_str)
        service_end_date.update([date_str[-4:] for date_str in matches_dd_mm_yyyy])
        service_end_date.update([date_str[:4] for date_str in matches_yyyy_mm_dd])

    service_end_date = sorted({str(int(end_date)) for end_date in service_end_date if end_date.isdigit()})
    if empty_found_end_date:
        service_end_date.insert(0, None)

    # Построение запроса
    # query = await sync_to_async(Services.objects.all)()
    query = await sync_to_async(lambda: Services.objects.all())()
    query_user = await sync_to_async(lambda: ServicesVault.objects.all())()
    query_user_two = await sync_to_async(lambda: ServicesTwo.objects.all())()

    if contract_date == 'No':
        contract_date = None
    if end_date == 'No':
        end_date = None

    if contract_date == 'None' and end_date == 'None':
        query = await sync_to_async(query.exclude)(Q(contract_date__regex=pattern_dd_mm_yyyy) | Q(contract_date__regex=pattern_yyyy_mm_dd) |
                            Q(end_date__regex=pattern_dd_mm_yyyy) | Q(end_date__regex=pattern_yyyy_mm_dd))
    elif contract_date == 'None' and end_date:
        query = await sync_to_async(query.exclude)(Q(contract_date__regex=pattern_dd_mm_yyyy) | Q(contract_date__regex=pattern_yyyy_mm_dd))
        query = await sync_to_async(query.filter)(end_date__icontains=end_date)
    elif contract_date == 'None' and not end_date:
        query = await sync_to_async(query.exclude)(Q(contract_date__regex=pattern_dd_mm_yyyy) | Q(contract_date__regex=pattern_yyyy_mm_dd))
    elif contract_date and end_date == 'None':
        query = await sync_to_async(query.exclude)(Q(end_date__regex=pattern_dd_mm_yyyy) | Q(end_date__regex=pattern_yyyy_mm_dd))
        query = await sync_to_async(query.filter)(contract_date__icontains=contract_date)
    elif not contract_date and end_date == 'None':
        query = await sync_to_async(query.exclude)(Q(end_date__regex=pattern_dd_mm_yyyy) | Q(end_date__regex=pattern_yyyy_mm_dd))
    elif contract_date and end_date:
        query = await sync_to_async(query.filter)(Q(contract_date__icontains=contract_date) | Q(end_date__icontains=end_date))
    elif contract_date and not end_date:
        query = await sync_to_async(query.filter)(contract_date__icontains=contract_date)
    elif not contract_date and end_date:
        query = await sync_to_async(query.filter)(end_date__icontains=end_date)

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

    if keyword_one:
        if selected_column_one and hasattr(Services, selected_column_one):
            query = await sync_to_async(query.filter)(**{selected_column_one + '__icontains': keyword_one})
        else:
            filters = Q()
            for field in await sync_to_async(Services._meta.get_fields)():
                filters |= Q(**{field.name + '__icontains': keyword_one})
            query = await sync_to_async(query.filter)(filters)

    if keyword_two:
        if selected_column_two and hasattr(Services, selected_column_two):
            query = await sync_to_async(query.filter)(**{selected_column_two + '__icontains': keyword_two})
        else:
            filters = Q()
            for field in await sync_to_async(Services._meta.get_fields)():
                filters |= Q(**{field.name + '__icontains': keyword_two})
            query = await sync_to_async(query.filter)(filters)

    if keyword_one_user:
        if selected_column_one_user and hasattr(Services, selected_column_one_user):
            query_user = await sync_to_async(query_user.filter)(**{selected_column_one_user + '__icontains': keyword_one_user})
        else:
            filters = Q()
            for field in await sync_to_async(Services._meta.get_fields)():
                filters |= Q(**{field.name + '__icontains': keyword_one_user})
            query_user = await sync_to_async(query_user.filter)(filters)

    if keyword_two_user:
        if selected_column_two_user and hasattr(Services, selected_column_two_user):
            query_user = await sync_to_async(query_user.filter)(**{selected_column_two_user + '__icontains': keyword_two_user})
        else:
            filters = Q()
            for field in await sync_to_async(Services._meta.get_fields)():
                filters |= Q(**{field.name + '__icontains': keyword_two_user})
            query_user = await sync_to_async(query_user.filter)(filters)

    if keyword_one_user_two:
        if selected_column_one_user_two and hasattr(ServicesTwo, selected_column_one_user_two):
            query_user_two = await sync_to_async(query_user_two.filter)(**{selected_column_one_user_two + '__icontains': keyword_one_user_two})
        else:
            filters = Q()
            for field in await sync_to_async(ServicesTwo._meta.get_fields)():
                filters |= Q(**{field.name + '__icontains': keyword_one_user_two})
            query_user_two = await sync_to_async(query_user_two.filter)(filters)

    if keyword_two_user_two:
        if selected_column_two_user and hasattr(ServicesTwo, selected_column_two_user_two):
            query_user_two = await sync_to_async(query_user_two.filter)(**{selected_column_two_user_two + '__icontains': keyword_two_user_two})
        else:
            filters = Q()
            for field in await sync_to_async(ServicesTwo._meta.get_fields)():
                filters |= Q(**{field.name + '__icontains': keyword_two_user_two})
            query_user_two = await sync_to_async(query_user_two.filter)(filters)

    # Сортировка
    # query = query.order_by('id_id', 'contract_date')

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
    # if contract_date == 'None' and end_date == 'None':
    #     total_cost_1 = await sync_to_async(query.exclude)(Q(year__regex=pattern_dd_mm_yyyy) | Q(year__regex=pattern_yyyy_mm_dd) |
    #                                 Q(date_number_no_one__regex=pattern_dd_mm_yyyy) | Q(date_number_no_one__regex=pattern_yyyy_mm_dd)).aggregate(Sum('cost'))['cost__sum'] or 0
    #     total_cost_2 = await sync_to_async(query.exclude)(Q(year__regex=pattern_dd_mm_yyyy) | Q(year__regex=pattern_yyyy_mm_dd) |
    #                                 Q(date_number_no_one__regex=pattern_dd_mm_yyyy) | Q(date_number_no_one__regex=pattern_yyyy_mm_dd)).aggregate(Sum('certificate'))['certificate__sum'] or 0
    #     total_cost_3 = await sync_to_async(query.exclude)(Q(year__regex=pattern_dd_mm_yyyy) | Q(year__regex=pattern_yyyy_mm_dd) |
    #                                 Q(date_number_no_one__regex=pattern_dd_mm_yyyy) | Q(date_number_no_one__regex=pattern_yyyy_mm_dd)).aggregate(Sum('certificate_no'))['certificate_no__sum'] or 0
    # elif contract_date and end_date:
    #     total_cost_1 = await sync_to_async(query.filter)(Q(year__icontains=contract_date) | Q(date_number_no_one__icontains=contract_date)).aggregate(Sum('cost'))['cost__sum'] or 0
    #     total_cost_2 = await sync_to_async(query.filter)(Q(year__icontains=contract_date) | Q(date_number_no_one__icontains=contract_date)).aggregate(Sum('certificate'))['certificate__sum'] or 0
    #     total_cost_3 = await sync_to_async(query.filter)(Q(year__icontains=contract_date) | Q(date_number_no_one__icontains=contract_date)).aggregate(Sum('certificate_no'))['certificate_no__sum'] or 0
    # elif contract_date == 'None' and end_date != 'None':
    #     total_cost_1 = await sync_to_async(query.exclude)(Q(year__regex=pattern_dd_mm_yyyy) | Q(year__regex=pattern_yyyy_mm_dd)).aggregate(Sum('cost'))['cost__sum'] or 0
    #     total_cost_2 = await sync_to_async(query.exclude)(Q(year__regex=pattern_dd_mm_yyyy) | Q(year__regex=pattern_yyyy_mm_dd)).aggregate(Sum('certificate'))['certificate__sum'] or 0
    #     total_cost_3 = await sync_to_async(query.exclude)(Q(year__regex=pattern_dd_mm_yyyy) | Q(year__regex=pattern_yyyy_mm_dd)).aggregate(Sum('certificate_no'))['certificate_no__sum'] or 0
    # elif contract_date and not end_date:
    #     total_cost_1 = await sync_to_async(query.filter)(Q(year__icontains=contract_date)).aggregate(Sum('cost'))['cost__sum'] or 0
    #     total_cost_2 = await sync_to_async(query.filter)(Q(year__icontains=contract_date)).aggregate(Sum('certificate'))['certificate__sum'] or 0
    #     total_cost_3 = await sync_to_async(query.filter)(Q(year__icontains=contract_date)).aggregate(Sum('certificate_no'))['certificate_no__sum'] or 0
    # elif contract_date != 'None' and end_date == 'None':
    #     total_cost_1 = await sync_to_async(query.exclude)(Q(date_number_no_one__regex=pattern_dd_mm_yyyy) | Q(date_number_no_one__regex=pattern_yyyy_mm_dd)).aggregate(Sum('cost'))['cost__sum'] or 0
    #     total_cost_2 = await sync_to_async(query.exclude)(Q(date_number_no_one__regex=pattern_dd_mm_yyyy) | Q(date_number_no_one__regex=pattern_yyyy_mm_dd)).aggregate(Sum('certificate'))['certificate__sum'] or 0
    #     total_cost_3 = await sync_to_async(query.exclude)(Q(date_number_no_one__regex=pattern_dd_mm_yyyy) | Q(date_number_no_one__regex=pattern_yyyy_mm_dd)).aggregate(Sum('certificate_no'))['certificate_no__sum'] or 0
    # elif not contract_date and end_date:
    #     total_cost_1 = await sync_to_async(query.filter)(Q(date_number_no_one__icontains=end_date)).aggregate(Sum('cost'))['cost__sum'] or 0
    #     total_cost_2 = await sync_to_async(query.filter)(Q(date_number_no_one__icontains=end_date)).aggregate(Sum('certificate'))['certificate__sum'] or 0
    #     total_cost_3 = await sync_to_async(query.filter)(Q(date_number_no_one__icontains=end_date)).aggregate(Sum('certificate_no'))['certificate_no__sum'] or 0
    # else:
    #     # total_cost_1 = query.aggregate(Sum('cost'))['cost__sum'] or 0
    #     total_cost_1 = await sync_to_async(lambda: query.aggregate(Sum('cost')))()
    #     total_cost_1 = total_cost_1['cost__sum'] or 0

    #     # total_cost_2 = query.aggregate(Sum('certificate'))['certificate__sum'] or 0
    #     total_cost_2 = await sync_to_async(lambda: query.aggregate(Sum('certificate')))()
    #     total_cost_2 = total_cost_2['certificate__sum'] or 0

    #     # total_cost_3 = query.aggregate(Sum('certificate_no'))['certificate_no__sum'] or 0
    #     total_cost_3 = await sync_to_async(lambda: query.aggregate(Sum('certificate_no')))()
    #     total_cost_3 = total_cost_3['certificate_no__sum'] or 0

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
        total_cost_18 = (total_cost_11 + total_cost_12) / total_cost_17
    except:
        total_cost_17 = 0
        total_cost_18 = 0

    # Пагинация
    paginator = Paginator(query, per_page)
    services = await sync_to_async(paginator.get_page)(page)

    # Пагинация
    paginator_user = Paginator(query_user, 30)
    services_user = await sync_to_async(paginator_user.get_page)(page_user)

    # Пагинация
    paginator_user_two = Paginator(query_user_two, per_page)
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
    # # Оборачиваем доступ к request.user.id в sync_to_async
    # user_id = await sync_to_async(lambda: request.user.id)()

    # # Оборачиваем print в sync_to_async
    # await sync_to_async(print)('user_id', user_id)

    # if user_id == 4:

    total_pages_full = request.GET.get('total_pages_full', None)

    if total_pages_full:
        per_page = 20
        # query = await sync_to_async(Services.objects.all())
        query = await sync_to_async(lambda: Services.objects.all())()
        # total_services_full = query.count()
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
        # query = await sync_to_async(Services.objects.all())
        query_user = await sync_to_async(lambda: ServicesVault.objects.all())()
        # total_services_full = query.count()
        total_services_full_user = await sync_to_async(lambda: query_user.count())()
        page_user = (total_services_full_user + per_page - 1) // per_page
    else:
        page_user = int(request.GET.get('page_user', 1))

    total_pages_full_user_two = request.GET.get('total_pages_full_user_two', None)

    if total_pages_full_user_two:
        per_page = 20
        # query = await sync_to_async(Services.objects.all())
        query_user_two = await sync_to_async(lambda: ServicesTwo.objects.all())()
        # total_services_full = query.count()
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

async def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            await User.objects.create_user(username=username, email=email, password=password)
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

    # return JsonResponse({'success': True, 'id': service.id, 'color': service.color})
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

    # return JsonResponse({'success': True, 'id': service.id, 'color': service.color})
    user = request.user

    # # Получаем объект service по id
    # service = get_object_or_404(Services, id=row_id)  # Измените на id_id, если используете поле id_id
    service = await sync_to_async(Services.objects.get)(id=row_id)

    # Подготовка контекста для шаблона
    context = {
        'service': service,
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

    # return JsonResponse({'success': True, 'id': service.id, 'color': service.color})
    user = request.user

    # # Получаем объект service по id
    # service = get_object_or_404(Services, id=row_id)  # Измените на id_id, если используете поле id_id
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

    # return JsonResponse({'success': True, 'id': service.id, 'color': service.color})
    user = request.user

    # # Получаем объект service по id
    # service = get_object_or_404(Services, id=row_id)  # Измените на id_id, если используете поле id_id
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

from urllib.parse import urlencode

@csrf_exempt  # Необходимо, если вы не используете CSRF-токены
async def update_record(request, row_id):
    if request.method == 'POST':
        try:
            data = request.POST

            id_id = data.get('id_id')
            name = data.get('name')
            status = data.get('status')
            way = data.get('way')
            initiator = data.get('initiator')
            KTSSR = data.get('KTSSR')
            KOSGU = data.get('KOSGU')
            DopFC = data.get('DopFC')
            NMCC = data.get('NMCC')
            saving = data.get('saving')
            counterparty = data.get('counterparty')
            registration_number = data.get('registration_number')
            contract_number = data.get('contract_number')
            contract_date = data.get('contract_date')
            end_date = data.get('end_date')
            contract_price = data.get('contract_price')
            # execution_contract_plan = data.get('execution_contract_plan')
            january_one = data.get('january_one')
            february = data.get('february')
            march = data.get('march')
            april = data.get('april')
            may = data.get('may')
            june = data.get('june')
            july = data.get('july')
            august = data.get('august')
            september = data.get('september')
            october = data.get('october')
            november = data.get('november')
            december = data.get('december')
            january_two = data.get('january_two')
            # execution_contract_fact = data.get('execution_contract_fact')
            date_january_one = data.get('date_january_one')
            sum_january_one = data.get('sum_january_one')
            date_february = data.get('date_february')
            sum_february = data.get('sum_february')
            date_march = data.get('date_march')
            sum_march = data.get('sum_march')
            date_april = data.get('date_april')
            sum_april = data.get('sum_april')
            date_may = data.get('date_may')
            sum_may = data.get('sum_may')
            date_june = data.get('date_june')
            sum_june = data.get('sum_june')
            date_july = data.get('date_july')
            sum_july = data.get('sum_july')
            date_august = data.get('date_august')
            sum_august = data.get('sum_august')
            date_september = data.get('date_september')
            sum_september = data.get('sum_september')
            date_october = data.get('date_october')
            sum_october = data.get('sum_october')
            date_november = data.get('date_november')
            sum_november = data.get('sum_november')
            date_december = data.get('date_december')
            sum_december = data.get('sum_december')
            date_january_two = data.get('date_january_two')
            sum_january_two = data.get('sum_january_two')
            execution = data.get('execution')
            contract_balance = data.get('contract_balance')
            color = data.get('color')

            execution_contract_plan = float(january_one) + float(february) + float(march)
            + float(april) + float(may) + float(june) + float(july) + float(august)
            + float(september) + float(october) + float(november) + float(december)
            + float(january_two)

            execution_contract_fact = float(sum_january_one) + float(sum_february) + float(sum_march)
            + float(sum_april) + float(sum_may) + float(sum_june) + float(sum_july) + float(sum_august)
            + float(sum_september) + float(sum_october) + float(sum_november) + float(sum_december)
            + float(sum_january_two)

            execution = float(execution_contract_fact) / float(contract_price)

            contract_balance = float(contract_price) - float(execution_contract_fact)

            # if certificate == '0' and certificate_no == '0':
            #     color = '#dff0d8'

            # user = request.user

            page = int(request.GET.get('page', 1))
            keyword_one = request.GET.get('keyword_one', None)
            keyword_two = request.GET.get('keyword_two', None)
            selected_column_one = request.GET.get('selected_column_one', None)
            selected_column_two = request.GET.get('selected_column_two', None)

            # keyword_one = None
            # keyword_two = None
            # selected_column_one=None
            # selected_column_two=None
            # page = 2

            # # return JsonResponse({'success': True, 'id': service.id, 'color': service.color})
            # user = request.user

            # return await skeleton(request, user, date_number_no_one, year, keyword_one, keyword_two, selected_column_one, selected_column_two, page)

            page_user = 1
            KOSGU_user = None
            keyword_one_user = None
            keyword_two_user = None
            selected_column_one_user = None
            selected_column_two_user = None

            page_user_two = 1
            KOSGU_user_two = None
            keyword_one_user_two = None
            keyword_two_user_two = None
            selected_column_one_user_two = None
            selected_column_two_user_two = None

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

            from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

            try:
                ServicesVault_ = await sync_to_async(Services.objects.get)(name=name)
                # await sync_to_async(messages.error)(request, 'Вы добавляете дубликат в Наименовании')


                # # Перенаправление с несколькими параметрами
                # return redirect(f"/?{urlencode(query_params)}")
            except MultipleObjectsReturned:
                ServicesVault_ = await sync_to_async(lambda: Services.objects.filter(name=name).first())()
                await sync_to_async(messages.error)(request, 'Вы добавляете дубликат в Ниименовании')


                # Перенаправление с несколькими параметрами
                return redirect(f"/?{urlencode(query_params)}")
            except ObjectDoesNotExist:
                pass

            from django.db.models import Q
            # Services_ = await sync_to_async(Services.objects.get)(
            #     Q(KOSGU='221') & Q(DopFC='0000000')
            # )
            Services_ = await sync_to_async(list)(Services.objects.filter(
                Q(KOSGU=KOSGU) & Q(DopFC=DopFC) & Q(KTSSR=KTSSR) & Q(status=status)
            ))
            contract_price_sum = 0
            execution_contract_fact_sum = 0
            for service in Services_:
                contract_price_sum += float(service.contract_price if service.contract_price not in [None, 'None', ''] else 0)
                execution_contract_fact_sum += float(service.execution_contract_fact if service.execution_contract_fact not in [None, 'None', ''] else 0)

            # # Найдите запись по ID
            # # ServicesVault_ = await sync_to_async(ServicesVault.objects.get)(KOSGU=KOSGU)

            try:
                ServicesVault_ = await sync_to_async(ServicesVault.objects.get)(
                    Q(KOSGU=KOSGU) & Q(DopFC=DopFC)
                )
            except:
                await sync_to_async(messages.error)(request, 'Нет сопоставления КОСГУ с ДопФК')

                # Перенаправление с несколькими параметрами
                return redirect(f"/?{urlencode(query_params)}")
            # ServicesVault_ = await sync_to_async(list)(ServicesVault.objects.filter(
            #     Q(KOSGU=KOSGU) & Q(DopFC=DopFC)
            # ))

            # print(KOSGU)
            # print(DopFC)
            # print('POPAL', ServicesVault_)
            # exit()

            if status == 'В торгах' and KTSSR == '2016100092':
                ServicesVault_.off_budget_bargaining = contract_price_sum
            elif status == 'В торгах' and KTSSR == '2016100000':
                ServicesVault_.budget_bargaining = contract_price_sum
            elif status == 'Запланировано' and KTSSR == '2016100092':
                ServicesVault_.off_budget_planned = contract_price_sum
            elif status == 'Запланировано' and KTSSR == '2016100000':
                ServicesVault_.budget_planned = contract_price_sum
            elif status == 'Заключено' and KTSSR == '2016100092':
                ServicesVault_.off_budget_concluded = contract_price_sum
            elif status == 'Заключено' and KTSSR == '2016100000':
                ServicesVault_.budget_concluded = contract_price_sum
            elif status == 'Исполнено' and KTSSR == '2016100092':
                ServicesVault_.off_budget_completed = contract_price_sum
            elif status == 'Исполнено' and KTSSR == '2016100000':
                ServicesVault_.budget_completed = contract_price_sum

            if KTSSR == '2016100092':
                ServicesVault_.off_budget_execution = execution_contract_fact_sum
            elif KTSSR == '2016100000':
                ServicesVault_.budget_execution = execution_contract_fact_sum

            ServicesVault_.budget_remainder = float(ServicesVault_.budget_limit if ServicesVault_.budget_limit not in [None, 'None', ''] else 0) - float(ServicesVault_.budget_bargaining if ServicesVault_.budget_bargaining not in [None, 'None', ''] else 0)
            - float(ServicesVault_.budget_concluded if ServicesVault_.budget_concluded not in [None, 'None', ''] else 0) - float(ServicesVault_.budget_completed if ServicesVault_.budget_completed not in [None, 'None', ''] else 0)
            ServicesVault_.off_budget_remainder = float(ServicesVault_.off_budget_limit if ServicesVault_.off_budget_limit not in [None, 'None', ''] else 0) - float(ServicesVault_.off_budget_bargaining if ServicesVault_.off_budget_bargaining not in [None, 'None', ''] else 0)
            - float(ServicesVault_.off_budget_concluded if ServicesVault_.off_budget_concluded not in [None, 'None', ''] else 0) - float(ServicesVault_.off_budget_completed if ServicesVault_.off_budget_completed not in [None, 'None', ''] else 0)

            ServicesVault_.budget_plans = float(ServicesVault_.budget_remainder if ServicesVault_.budget_remainder not in [None, 'None', ''] else 0) - float(ServicesVault_.budget_planned if ServicesVault_.budget_planned not in [None, 'None', ''] else 0)
            ServicesVault_.off_budget_plans = float(ServicesVault_.off_budget_remainder if ServicesVault_.off_budget_remainder not in [None, 'None', ''] else 0) - float(ServicesVault_.off_budget_planned if ServicesVault_.off_budget_planned not in [None, 'None', ''] else 0)

            if any(x < 0 for x in [ServicesVault_.budget_remainder, ServicesVault_.off_budget_remainder, ServicesVault_.budget_plans, ServicesVault_.off_budget_plans]):
                ServicesVault_.color = '#ffebeb'
                color = '#ffebeb'
            else:
                ServicesVault_.color = ''
                color = ''

            await sync_to_async(ServicesVault_.save)()

            # Найдите запись по ID и обновите цвет
            service = await sync_to_async(Services.objects.get)(id=row_id)

            service.id_id = id_id
            service.name = name
            service.status = status
            service.way = way
            service.initiator = initiator
            service.KTSSR = KTSSR
            service.KOSGU = KOSGU
            service.DopFC = DopFC
            service.NMCC = NMCC
            service.saving = saving
            service.counterparty = counterparty
            service.registration_number = registration_number
            service.contract_number = contract_number
            service.contract_date = contract_date
            service.end_date = end_date
            service.contract_price = contract_price
            service.execution_contract_plan = execution_contract_plan
            service.january_one = january_one
            service.february = february
            service.march = march
            service.april = april
            service.may = may
            service.june = june
            service.july = july
            service.august = august
            service.september = september
            service.october = october
            service.november = november
            service.december = december
            service.january_two = january_two
            service.execution_contract_fact = execution_contract_fact
            service.date_january_one = date_january_one
            service.sum_january_one = sum_january_one
            service.date_february = date_february
            service.sum_february = sum_february
            service.date_march = date_march
            service.sum_march = sum_march
            service.date_april = date_april
            service.sum_april = sum_april
            service.date_may = date_may
            service.sum_may = sum_may
            service.date_june = date_june
            service.sum_june = sum_june
            service.date_july = date_july
            service.sum_july = sum_july
            service.date_august = date_august
            service.sum_august = sum_august
            service.date_september = date_september
            service.sum_september = sum_september
            service.date_october = date_october
            service.sum_october = sum_october
            service.date_november = date_november
            service.sum_november = sum_november
            service.date_december = date_december
            service.sum_december = sum_december
            service.date_january_two = date_january_two
            service.sum_january_two = sum_january_two
            service.execution = execution
            service.contract_balance = contract_balance
            service.color = color

            await sync_to_async(service.save)()

            await sync_to_async(messages.success)(request, "Редактирование прошло успешно.")

            # Перенаправление с несколькими параметрами
            return redirect(f"/?{urlencode(query_params)}")

            # return await skeleton(request, user, contract_date, end_date, keyword_one, keyword_two, selected_column_one, selected_column_two, page, KOSGU_user, keyword_one_user, keyword_two_user, selected_column_one_user, selected_column_two_user, page_user)

        except Services.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Service not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON.'}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)

@csrf_exempt  # Необходимо, если вы не используете CSRF-токены
async def update_record_user(request, row_id):
    if request.method == 'POST':
        try:
            data = request.POST

            id_id = data.get('id_id')
            name = data.get('name')
            KOSGU = data.get('KOSGU')
            DopFC = data.get('DopFC')
            budget_limit = data.get('budget_limit')
            off_budget_limit = data.get('off_budget_limit')
            budget_planned = data.get('budget_planned')
            off_budget_planned = data.get('off_budget_planned')
            budget_bargaining = data.get('budget_bargaining')
            off_budget_bargaining = data.get('off_budget_bargaining')
            budget_concluded = data.get('budget_concluded')
            off_budget_concluded = data.get('off_budget_concluded')
            budget_completed = data.get('budget_completed')
            off_budget_completed = data.get('off_budget_completed')
            budget_execution = data.get('budget_execution')
            off_budget_execution = data.get('off_budget_execution')
            budget_remainder = data.get('budget_remainder')
            off_budget_remainder = data.get('off_budget_remainder')
            budget_plans = data.get('budget_plans')
            off_budget_plans = data.get('off_budget_plans')
            color = data.get('color')

            # Найдите запись по ID и обновите цвет
            service = await sync_to_async(ServicesVault.objects.get)(id=row_id)

            service.id_id = id_id
            service.name = name
            service.KOSGU = KOSGU
            service.DopFC = DopFC
            service.budget_limit = budget_limit
            service.off_budget_limit = off_budget_limit
            service.budget_planned = budget_planned
            service.off_budget_planned = off_budget_planned
            service.budget_bargaining = budget_bargaining
            service.off_budget_bargaining = off_budget_bargaining
            service.budget_concluded = budget_concluded
            service.off_budget_concluded = off_budget_concluded
            service.budget_completed = budget_completed
            service.off_budget_completed = off_budget_completed
            service.budget_execution = budget_execution
            service.off_budget_execution = off_budget_execution
            service.budget_remainder = budget_remainder
            service.off_budget_remainder = off_budget_remainder
            service.budget_plans = budget_plans
            service.off_budget_plans = off_budget_plans
            service.color = color

            await sync_to_async(service.save)()

            try:
                ServicesVault_ = await sync_to_async(ServicesVault.objects.get)(
                    Q(KOSGU=KOSGU) & Q(DopFC=DopFC)
                )

                ServicesVault_.budget_remainder = float(ServicesVault_.budget_limit if ServicesVault_.budget_limit not in [None, 'None', ''] else 0) - float(ServicesVault_.budget_bargaining if ServicesVault_.budget_bargaining not in [None, 'None', ''] else 0)
                - float(ServicesVault_.budget_concluded if ServicesVault_.budget_concluded not in [None, 'None', ''] else 0) - float(ServicesVault_.budget_completed if ServicesVault_.budget_completed not in [None, 'None', ''] else 0)
                ServicesVault_.off_budget_remainder = float(ServicesVault_.off_budget_limit if ServicesVault_.off_budget_limit not in [None, 'None', ''] else 0) - float(ServicesVault_.off_budget_bargaining if ServicesVault_.off_budget_bargaining not in [None, 'None', ''] else 0)
                - float(ServicesVault_.off_budget_concluded if ServicesVault_.off_budget_concluded not in [None, 'None', ''] else 0) - float(ServicesVault_.off_budget_completed if ServicesVault_.off_budget_completed not in [None, 'None', ''] else 0)

                await sync_to_async(ServicesVault_.save)()
            except:
                pass

            await sync_to_async(messages.success)(request, "Редактирование прошло успешно.")

            page = 1
            keyword_one = None
            keyword_two = None
            selected_column_one = None
            selected_column_two = None

            # keyword_one = None
            # keyword_two = None
            # selected_column_one=None
            # selected_column_two=None
            # page = 2

            # # return JsonResponse({'success': True, 'id': service.id, 'color': service.color})
            # user = request.user

            # return await skeleton(request, user, date_number_no_one, year, keyword_one, keyword_two, selected_column_one, selected_column_two, page)

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

            # return await skeleton(request, user, contract_date, end_date, keyword_one, keyword_two, selected_column_one, selected_column_two, page, KOSGU_user, keyword_one_user, keyword_two_user, selected_column_one_user, selected_column_two_user, page_user)

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

                ServicesVault_ = await sync_to_async(ServicesVault.objects.get)(
                    Q(KOSGU=KOSGU) & Q(DopFC=DopFC)
                )

                ServicesVault_.budget_plans = float(ServicesVault_.budget_remainder if ServicesVault_.budget_remainder not in [None, 'None', ''] else 0) - float(ServicesVault_.budget_planned if ServicesVault_.budget_planned not in [None, 'None', ''] else 0)
                ServicesVault_.off_budget_plans = float(ServicesVault_.off_budget_remainder if ServicesVault_.off_budget_remainder not in [None, 'None', ''] else 0) - float(ServicesVault_.off_budget_planned if ServicesVault_.off_budget_planned not in [None, 'None', ''] else 0)

                await sync_to_async(ServicesVault_.save)()
            except:
                pass

            await sync_to_async(messages.success)(request, "Редактирование прошло успешно.")

            page = 1
            keyword_one = None
            keyword_two = None
            selected_column_one = None
            selected_column_two = None

            # keyword_one = None
            # keyword_two = None
            # selected_column_one=None
            # selected_column_two=None
            # page = 2

            # # return JsonResponse({'success': True, 'id': service.id, 'color': service.color})
            # user = request.user

            # return await skeleton(request, user, date_number_no_one, year, keyword_one, keyword_two, selected_column_one, selected_column_two, page)

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

            # return await skeleton(request, user, contract_date, end_date, keyword_one, keyword_two, selected_column_one, selected_column_two, page, KOSGU_user, keyword_one_user, keyword_two_user, selected_column_one_user, selected_column_two_user, page_user)

        except Services.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Service not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON.'}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)

@csrf_exempt  # Необходимо, если вы не используете CSRF-токены
async def add_record(request):

    if request.method == 'POST':
        try:
            total_pages = int(request.GET.get('total_pages', 1))

            name = request.POST['name']
            status = request.POST['status']
            way = request.POST['way']
            initiator = request.POST['initiator']
            KTSSR = request.POST['KTSSR']
            KOSGU = request.POST['KOSGU']
            DopFC = request.POST['DopFC']
            NMCC = request.POST['NMCC']
            saving = request.POST['saving']
            counterparty = request.POST['counterparty']
            registration_number = request.POST['registration_number']
            contract_number = request.POST['contract_number']
            contract_date = request.POST['contract_date']
            end_date = request.POST['end_date']
            contract_price = request.POST['contract_price']
            # execution_contract_plan = request.POST['execution_contract_plan']
            january_one = request.POST['january_one']
            february = request.POST['february']
            march = request.POST['march']
            april = request.POST['april']
            may = request.POST['may']
            june = request.POST['june']
            july = request.POST['july']
            august = request.POST['august']
            september = request.POST['september']
            october = request.POST['october']
            november = request.POST['november']
            december = request.POST['december']
            january_two = request.POST['january_two']
            # execution_contract_fact = request.POST['execution_contract_fact']
            date_january_one = request.POST['date_january_one']
            sum_january_one = request.POST['sum_january_one']
            date_february = request.POST['date_february']
            sum_february = request.POST['sum_february']
            date_march = request.POST['date_march']
            sum_march = request.POST['sum_march']
            date_april = request.POST['date_april']
            sum_april = request.POST['sum_april']
            date_may = request.POST['date_may']
            sum_may = request.POST['sum_may']
            date_june = request.POST['date_june']
            sum_june = request.POST['sum_june']
            date_july = request.POST['date_july']
            sum_july = request.POST['sum_july']
            date_august = request.POST['date_august']
            sum_august = request.POST['sum_august']
            date_september = request.POST['date_september']
            sum_september = request.POST['sum_september']
            date_october = request.POST['date_october']
            sum_october = request.POST['sum_october']
            date_november = request.POST['date_november']
            sum_november = request.POST['sum_november']
            date_december = request.POST['date_december']
            sum_december = request.POST['sum_december']
            date_january_two = request.POST['date_january_two']
            sum_january_two = request.POST['sum_january_two']
            # execution = request.POST['execution']
            # contract_balance = request.POST['contract_balance']
            color = request.POST.get('color')

            execution_contract_plan = float(january_one) + float(february) + float(march)
            + float(april) + float(may) + float(june) + float(july) + float(august)
            + float(september) + float(october) + float(november) + float(december)
            + float(january_two)

            execution_contract_fact = float(sum_january_one) + float(sum_february) + float(sum_march)
            + float(sum_april) + float(sum_may) + float(sum_june) + float(sum_july) + float(sum_august)
            + float(sum_september) + float(sum_october) + float(sum_november) + float(sum_december)
            + float(sum_january_two)

            execution = float(execution_contract_fact) / float(contract_price)

            contract_balance = float(contract_price) - float(execution_contract_fact)

            # if certificate == '0' and certificate_no == '0':
            #     color = '#dff0d8'

            # user = request.user

            keyword_one = None
            keyword_two = None
            selected_column_one=None
            selected_column_two=None
            page = total_pages

            # return await skeleton(request, user, date_number_no_one, year, keyword_one, keyword_two, selected_column_one, selected_column_two, page)

            page_user = 1

            KOSGU_user = request.GET.get('KOSGU_user', None)
            keyword_one_user = request.GET.get('keyword_one_user', None)
            keyword_two_user = request.GET.get('keyword_two_user', None)
            selected_column_one_user = request.GET.get('selected_column_one_user', None)
            selected_column_two_user = request.GET.get('selected_column_two_user', None)

            page_user_two = 1

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

            from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

            try:
                Services_ = await sync_to_async(Services.objects.get)(name=name)
                await sync_to_async(messages.error)(request, 'Вы добавляете дубликат в Наименовании')

                # Перенаправление с несколькими параметрами
                return redirect(f"/?{urlencode(query_params)}")
            except MultipleObjectsReturned:
                Services_ = await sync_to_async(lambda: Services.objects.filter(name=name).first())()
                await sync_to_async(messages.error)(request, 'Вы добавляете дубликат в Ниименовании')

                # Перенаправление с несколькими параметрами
                return redirect(f"/?{urlencode(query_params)}")
            except ObjectDoesNotExist:
                pass

            from django.db.models import Q
            # Services_ = await sync_to_async(Services.objects.get)(
            #     Q(KOSGU='221') & Q(DopFC='0000000')
            # )
            Services_ = await sync_to_async(list)(Services.objects.filter(
                Q(KOSGU=KOSGU) & Q(DopFC=DopFC) & Q(KTSSR=KTSSR) & Q(status=status)
            ))
            contract_price_sum = 0
            execution_contract_fact_sum = 0
            for service in Services_:
                contract_price_sum += float(service.contract_price if service.contract_price not in [None, 'None', ''] else 0)
                execution_contract_fact_sum += float(service.execution_contract_fact if service.execution_contract_fact not in [None, 'None', ''] else 0)

            # # Найдите запись по ID
            # # ServicesVault_ = await sync_to_async(ServicesVault.objects.get)(KOSGU=KOSGU)

            try:
                ServicesVault_ = await sync_to_async(ServicesVault.objects.get)(
                    Q(KOSGU=KOSGU) & Q(DopFC=DopFC)
                )
            except:
                await sync_to_async(messages.error)(request, 'Нет сопоставления КОСГУ с ДопФК')

                # Перенаправление с несколькими параметрами
                return redirect(f"/?{urlencode(query_params)}")
            # ServicesVault_ = await sync_to_async(list)(ServicesVault.objects.filter(
            #     Q(KOSGU=KOSGU) & Q(DopFC=DopFC)
            # ))

            try:

                if way == 'п.4 ч.1 ст.93':
                    ServicesTwo_ = await sync_to_async(ServicesTwo.objects.get)(
                        Q(KOSGU=KOSGU) & Q(DopFC=DopFC)
                    )

                    if status == 'Заключено' and KTSSR == '2016100092':
                        ServicesTwo_.off_budget_concluded = contract_price_sum
                        ServicesTwo_.off_budget_remainder = float(ServicesTwo_.off_budget_planned) - float(contract_price_sum)
                    elif status == 'Заключено' and KTSSR == '2016100000':
                        ServicesTwo_.budget_concluded = contract_price_sum
                        ServicesTwo_.budget_remainder = float(ServicesTwo_.budget_planned) - float(contract_price_sum)

                    if any(x < 0 for x in [ServicesVault_.budget_remainder, ServicesVault_.off_budget_remainder, ServicesVault_.budget_plans, ServicesVault_.off_budget_plans]):
                        ServicesTwo_.color = '#ffebeb'
                    else:
                        ServicesTwo_.color = ''

                    await sync_to_async(ServicesTwo_.save)()

            except:
                pass

            # print(KOSGU)
            # print(DopFC)
            # print('POPAL', ServicesVault_)
            # exit()

            if status == 'В торгах' and KTSSR == '2016100092':
                ServicesVault_.off_budget_bargaining = contract_price_sum
            elif status == 'В торгах' and KTSSR == '2016100000':
                ServicesVault_.budget_bargaining = contract_price_sum
            elif status == 'Запланировано' and KTSSR == '2016100092':
                ServicesVault_.off_budget_planned = contract_price_sum
            elif status == 'Запланировано' and KTSSR == '2016100000':
                ServicesVault_.budget_planned = contract_price_sum
            elif status == 'Заключено' and KTSSR == '2016100092':
                ServicesVault_.off_budget_concluded = contract_price_sum
            elif status == 'Заключено' and KTSSR == '2016100000':
                ServicesVault_.budget_concluded = contract_price_sum
            elif status == 'Исполнено' and KTSSR == '2016100092':
                ServicesVault_.off_budget_completed = contract_price_sum
            elif status == 'Исполнено' and KTSSR == '2016100000':
                ServicesVault_.budget_completed = contract_price_sum

            if KTSSR == '2016100092':
                ServicesVault_.off_budget_execution = execution_contract_fact_sum
            elif KTSSR == '2016100000':
                ServicesVault_.budget_execution = execution_contract_fact_sum

            ServicesVault_.budget_remainder = float(ServicesVault_.budget_limit if ServicesVault_.budget_limit not in [None, 'None', ''] else 0) - float(ServicesVault_.budget_bargaining if ServicesVault_.budget_bargaining not in [None, 'None', ''] else 0)
            - float(ServicesVault_.budget_concluded if ServicesVault_.budget_concluded not in [None, 'None', ''] else 0) - float(ServicesVault_.budget_completed if ServicesVault_.budget_completed not in [None, 'None', ''] else 0)
            ServicesVault_.off_budget_remainder = float(ServicesVault_.off_budget_limit if ServicesVault_.off_budget_limit not in [None, 'None', ''] else 0) - float(ServicesVault_.off_budget_bargaining if ServicesVault_.off_budget_bargaining not in [None, 'None', ''] else 0)
            - float(ServicesVault_.off_budget_concluded if ServicesVault_.off_budget_concluded not in [None, 'None', ''] else 0) - float(ServicesVault_.off_budget_completed if ServicesVault_.off_budget_completed not in [None, 'None', ''] else 0)

            ServicesVault_.budget_plans = float(ServicesVault_.budget_remainder if ServicesVault_.budget_remainder not in [None, 'None', ''] else 0) - float(ServicesVault_.budget_planned if ServicesVault_.budget_planned not in [None, 'None', ''] else 0)
            ServicesVault_.off_budget_plans = float(ServicesVault_.off_budget_remainder if ServicesVault_.off_budget_remainder not in [None, 'None', ''] else 0) - float(ServicesVault_.off_budget_planned if ServicesVault_.off_budget_planned not in [None, 'None', ''] else 0)

            if any(x < 0 for x in [ServicesVault_.budget_remainder, ServicesVault_.off_budget_remainder, ServicesVault_.budget_plans, ServicesVault_.off_budget_plans]):
                ServicesVault_.color = '#ffebeb'
                ServicesTwo_.color = '#ffebeb'
                color = '#ffebeb'
            else:
                ServicesVault_.color = ''
                ServicesTwo_.color = ''
                color = ''

            await sync_to_async(ServicesVault_.save)()

            # if way == 'п.4 ч.1 ст.93':

            #     # ServicesVault.DopFC = 'DopFC'
            #     # ServicesVault.budget_limit = 'budget_limit'
            #     # ServicesVault.off_budget_limit = 'off_budget_limit'
            #     # ServicesVault.budget_planned = 'budget_planned'
            #     # ServicesVault.off_budget_planned = 'off_budget_planned'
            #     ServicesVault_.budget_concluded = contract_price
            #     # ServicesVault.off_budget_concluded = 'off_budget_concluded'
            #     # ServicesVault.budget_completed = 'budget_completed'
            #     # ServicesVault.off_budget_completed = 'off_budget_completed'
            #     # ServicesVault.budget_execution = 'budget_execution'
            #     # ServicesVault.off_budget_execution = 'off_budget_execution'
            #     # ServicesVault.budget_remainder = 'budget_remainder'
            #     # ServicesVault.off_budget_remainder = 'off_budget_remainder'
            #     # ServicesVault.budget_plans = 'budget_plans'
            #     # ServicesVault.off_budget_plans = 'off_budget_plans'

            #     await sync_to_async(ServicesVault_.save)()

            # Получаем следующий ID
            # latest_service = await sync_to_async(Services.objects.order_by('-id_id').first)()
            from django.db import connection

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

            new_service = Services(id_id=id_id, name=name, status=status, way=way,
                                initiator=initiator, KTSSR=KTSSR, KOSGU=KOSGU,
                                DopFC=DopFC, NMCC=NMCC, saving=saving,
                                counterparty=counterparty, registration_number=registration_number,
                                contract_number=contract_number, contract_date=contract_date,
                                end_date=end_date, contract_price=contract_price, execution_contract_plan=execution_contract_plan,
                                january_one=january_one, february=february, march=march, april=april,
                                may=may, june=june, july=july, august=august,
                                september=september, october=october, november=november, december=december,
                                january_two=january_two, execution_contract_fact=execution_contract_fact, date_january_one=date_january_one,
                                sum_january_one=sum_january_one, date_february=date_february, sum_february=sum_february,
                                date_march=date_march, sum_march=sum_march, date_april=date_april,
                                sum_april=sum_april, date_may=date_may, sum_may=sum_may,
                                date_june=date_june, sum_june=sum_june, date_july=date_july,
                                sum_july=sum_july, date_august=date_august, sum_august=sum_august,
                                date_september=date_september, sum_september=sum_september, date_october=date_october,
                                sum_october=sum_october, date_november=date_november, sum_november=sum_november,
                                date_december=date_december, sum_december=sum_december, date_january_two=date_january_two,
                                sum_january_two=sum_january_two, execution=execution, contract_balance=contract_balance,
                                color=color)

            await sync_to_async(new_service.save)()
            await sync_to_async(messages.success)(request, 'Данные успешно добавлены!')

            # Перенаправление с несколькими параметрами
            return redirect(f"/?{urlencode(query_params)}")

            # return await skeleton(request, user, contract_date, end_date, keyword_one, keyword_two, selected_column_one, selected_column_two, page, KOSGU_user, keyword_one_user, keyword_two_user, selected_column_one_user, selected_column_two_user, page_user)
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

            KOSGU = service.KOSGU

            DopFC = service.DopFC

            KTSSR = service.KTSSR

            status = service.status

            way = service.way

            try:

                if way == 'п.4 ч.1 ст.93':
                    ServicesTwo_ = await sync_to_async(ServicesTwo.objects.get)(
                        Q(KOSGU=KOSGU) & Q(DopFC=DopFC)
                    )

                    if status == 'Заключено' and KTSSR == '2016100092':
                        ServicesTwo_.off_budget_concluded = contract_price_sum
                        ServicesTwo_.off_budget_remainder = float(ServicesTwo_.off_budget_planned) - float(contract_price_sum)
                    elif status == 'Заключено' and KTSSR == '2016100000':
                        ServicesTwo_.budget_concluded = contract_price_sum
                        ServicesTwo_.budget_remainder = float(ServicesTwo_.budget_planned) - float(contract_price_sum)

                    if any(x < 0 for x in [ServicesVault_.budget_remainder, ServicesVault_.off_budget_remainder, ServicesVault_.budget_plans, ServicesVault_.off_budget_plans]):
                        ServicesTwo_.color = '#ffebeb'
                    else:
                        ServicesTwo_.color = ''

                    await sync_to_async(ServicesTwo_.save)()

            except:
                pass

            try:
                from django.db.models import Q
                # Services_ = await sync_to_async(Services.objects.get)(
                #     Q(KOSGU='221') & Q(DopFC='0000000')
                # )
                Services_ = await sync_to_async(list)(Services.objects.filter(
                    Q(KOSGU=KOSGU) & Q(DopFC=DopFC) & Q(KTSSR=KTSSR) & Q(status=status)
                ))
                contract_price_sum = 0
                execution_contract_fact_sum = 0
                for service in Services_:
                    contract_price_sum += float(service.contract_price if service.contract_price not in [None, 'None', ''] else 0)
                    execution_contract_fact_sum += float(service.execution_contract_fact if service.execution_contract_fact not in [None, 'None', ''] else 0)

                ServicesVault_ = await sync_to_async(ServicesVault.objects.get)(
                    Q(KOSGU=KOSGU) & Q(DopFC=DopFC)
                )

                if status == 'В торгах' and KTSSR == '2016100092':
                    ServicesVault_.off_budget_bargaining = contract_price_sum
                elif status == 'В торгах' and KTSSR == '2016100000':
                    ServicesVault_.budget_bargaining = contract_price_sum
                elif status == 'Запланировано' and KTSSR == '2016100092':
                    ServicesVault_.off_budget_planned = contract_price_sum
                elif status == 'Запланировано' and KTSSR == '2016100000':
                    ServicesVault_.budget_planned = contract_price_sum
                elif status == 'Заключено' and KTSSR == '2016100092':
                    ServicesVault_.off_budget_concluded = contract_price_sum
                elif status == 'Заключено' and KTSSR == '2016100000':
                    ServicesVault_.budget_concluded = contract_price_sum
                elif status == 'Исполнено' and KTSSR == '2016100092':
                    ServicesVault_.off_budget_completed = contract_price_sum
                elif status == 'Исполнено' and KTSSR == '2016100000':
                    ServicesVault_.budget_completed = contract_price_sum

                if KTSSR == '2016100092':
                    ServicesVault_.off_budget_execution = execution_contract_fact_sum
                elif KTSSR == '2016100000':
                    ServicesVault_.budget_execution = execution_contract_fact_sum

                ServicesVault_.budget_remainder = float(ServicesVault_.budget_limit if ServicesVault_.budget_limit not in [None, 'None', ''] else 0) - float(ServicesVault_.budget_bargaining if ServicesVault_.budget_bargaining not in [None, 'None', ''] else 0)
                - float(ServicesVault_.budget_concluded if ServicesVault_.budget_concluded not in [None, 'None', ''] else 0) - float(ServicesVault_.budget_completed if ServicesVault_.budget_completed not in [None, 'None', ''] else 0)
                ServicesVault_.off_budget_remainder = float(ServicesVault_.off_budget_limit if ServicesVault_.off_budget_limit not in [None, 'None', ''] else 0) - float(ServicesVault_.off_budget_bargaining if ServicesVault_.off_budget_bargaining not in [None, 'None', ''] else 0)
                - float(ServicesVault_.off_budget_concluded if ServicesVault_.off_budget_concluded not in [None, 'None', ''] else 0) - float(ServicesVault_.off_budget_completed if ServicesVault_.off_budget_completed not in [None, 'None', ''] else 0)

                ServicesVault_.budget_plans = float(ServicesVault_.budget_remainder if ServicesVault_.budget_remainder not in [None, 'None', ''] else 0) - float(ServicesVault_.budget_planned if ServicesVault_.budget_planned not in [None, 'None', ''] else 0)
                ServicesVault_.off_budget_plans = float(ServicesVault_.off_budget_remainder if ServicesVault_.off_budget_remainder not in [None, 'None', ''] else 0) - float(ServicesVault_.off_budget_planned if ServicesVault_.off_budget_planned not in [None, 'None', ''] else 0)

                if any(x < 0 for x in [ServicesVault_.budget_remainder, ServicesVault_.off_budget_remainder, ServicesVault_.budget_plans, ServicesVault_.off_budget_plans]):
                    ServicesVault_.color = '#ffebeb'
                    ServicesTwo_.color = '#ffebeb'
                else:
                    ServicesVault_.color = ''
                    ServicesTwo_.color = ''

                await sync_to_async(ServicesVault_.save)()

            except:
                pass

            # Удаление записи
            await sync_to_async(service.delete)()

            # Сообщение об успешном удалении
            await sync_to_async(messages.success)(request, 'Данные успешно удалены!')

            # Перенаправление на главную страницу
            return redirect('data_table_view')
        except Services.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Service not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON.'}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)