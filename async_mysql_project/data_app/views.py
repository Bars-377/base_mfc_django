from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Services, ServicesVault
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

async def skeleton(request, user, contract_date, end_date, keyword_one, keyword_two, selected_column_one, selected_column_two, page, KOSGU_user, keyword_one_user, keyword_two_user, selected_column_one_user, selected_column_two_user, page_user):
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

    if KOSGU_user == 'None':
        query_user = await sync_to_async(query_user.exclude)(Q(KOSGU__regex=pattern_dd_mm_yyyy) | Q(KOSGU__regex=pattern_yyyy_mm_dd))
    elif KOSGU_user:
        query_user = await sync_to_async(query_user.filter)(KOSGU__icontains=KOSGU_user)

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

    # Пагинация
    paginator = Paginator(query, per_page)
    services = await sync_to_async(paginator.get_page)(page)

    # Пагинация
    paginator_user = Paginator(query_user, per_page)
    services_user = await sync_to_async(paginator_user.get_page)(page_user)

    # Получаем общее количество страниц
    total_pages = paginator.num_pages

    # Получаем общее количество страниц
    total_pages_user = paginator_user.num_pages

    # Определяем максимальное количество кнопок для навигации
    max_page_buttons = 5
    start_page = max(1, page - max_page_buttons // 2)
    end_page = min(total_pages, page + max_page_buttons // 2)

    # Определяем максимальное количество кнопок для навигации
    max_page_buttons_user = 5
    start_page_user = max(1, page_user - max_page_buttons_user // 2)
    end_page_user = min(total_pages_user, page_user + max_page_buttons_user // 2)

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

    pages = range(start_page, end_page + 1)  # Создаем диапазон страниц

    pages_user = range(start_page_user, end_page_user + 1)  # Создаем диапазон страниц

    # Подготовка контекста для шаблона
    context = {
        'data': services,
        'data_user': services_user,
        'user': user,
        'pages': pages,
        'pages_user': pages_user,
        # 'total_cost_1': total_cost_1,
        # 'total_cost_2': total_cost_2,
        # 'total_cost_3': total_cost_3,
        'selected_contract_date': contract_date,
        'selected_KOSGU_user': KOSGU_user,
        'selected_end_date': end_date,
        'selected_column_one': selected_column_one,
        'selected_column_one_user': selected_column_one_user,
        'selected_column_two': selected_column_two,
        'selected_column_two_user': selected_column_two_user,
        'keyword_one': keyword_one,
        'keyword_one_user': keyword_one_user,
        'keyword_two': keyword_two,
        'keyword_two_user': keyword_two_user,
        'page': page,
        'page_user': page_user,
        'total_pages': total_pages,
        'total_pages_user': total_pages_user,
        'start_page': start_page,
        'start_page_user': start_page_user,
        'end_page': end_page,
        'end_page_user': end_page_user,
        'service_years': service_years,
        'service_KOSGU_user': service_KOSGU_user,
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

    KOSGU_user = request.GET.get('KOSGU_user', None)
    keyword_one_user = request.GET.get('keyword_one_user', None)
    keyword_two_user = request.GET.get('keyword_two_user', None)
    selected_column_one_user = request.GET.get('selected_column_one_user', None)
    selected_column_two_user = request.GET.get('selected_column_two_user', None)

    return await skeleton(request, user, contract_date, end_date, keyword_one, keyword_two, selected_column_one, selected_column_two, page, KOSGU_user, keyword_one_user, keyword_two_user, selected_column_one_user, selected_column_two_user, page_user)

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
async def delete_record(request, row_id):
    if request.method == 'POST':
        try:
            # Найдите запись по ID и обновите цвет
            service = await sync_to_async(Services.objects.get)(id=row_id)

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

# from django.shortcuts import get_object_or_404

@csrf_exempt  # Необходимо, если вы не используете CSRF-токены
async def add(request):
    page = int(request.GET.get('page', 1))
    keyword_one = request.GET.get('keyword_one', None)
    keyword_two = request.GET.get('keyword_two', None)
    selected_column_one = request.GET.get('selected_column_one', None)
    selected_column_two = request.GET.get('selected_column_two', None)
    selected_year = request.GET.get('selected_year', "No")
    date_number_no_one = request.GET.get('date_number_no_one', "No")
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
        'selected_year': selected_year,
        'selected_date_number_no_one': date_number_no_one,
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
    selected_year = request.GET.get('selected_year', "No")
    date_number_no_one = request.GET.get('date_number_no_one', "No")

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
        'selected_year': selected_year,
        'selected_date_number_no_one': date_number_no_one
    }

    return await sync_to_async(render)(request, 'edit.html', context)

@csrf_exempt  # Необходимо, если вы не используете CSRF-токены
async def update_record(request, row_id):
    if request.method == 'POST':
        try:
            data = request.POST

            id_id = data.get('id_id')
            name = data.get('name')
            snils = data.get('snils')
            location = data.get('location')
            address_p = data.get('address_p')
            address = data.get('address')
            benefit = data.get('benefit')
            number = data.get('number')
            year = data.get('year')
            cost = data.get('cost')
            certificate = data.get('certificate')
            date_number_get = data.get('date_number_get')
            date_number_cancellation = data.get('date_number_cancellation')
            date_number_no_one = data.get('date_number_no_one')
            date_number_no_two = data.get('date_number_no_two')
            certificate_no = data.get('certificate_no')
            reason = data.get('reason')
            track = data.get('track')
            date_post = data.get('date_post')
            comment = data.get('comment')
            color = data.get('color')
            if certificate == '0' and certificate_no == '0':
                color = '#dff0d8'

            # Найдите запись по ID и обновите цвет
            service = await sync_to_async(Services.objects.get)(id=row_id)

            service.id_id = id_id
            service.name = name
            service.snils = snils
            service.location = location
            service.address_p = address_p
            service.address = address
            service.benefit = benefit
            service.number = number
            service.year = year
            service.cost = cost
            service.certificate = certificate
            service.date_number_get = date_number_get
            service.date_number_cancellation = date_number_cancellation
            service.date_number_no_one = date_number_no_one
            service.date_number_no_two = date_number_no_two
            service.certificate_no = certificate_no
            service.reason = reason
            service.track = track
            service.date_post = date_post
            service.comment = comment
            service.color = color

            await sync_to_async(service.save)()

            await sync_to_async(messages.success)(request, "Редактирование прошло успешно.")

            page = int(request.GET.get('page', 1))
            keyword_one = request.GET.get('keyword_one', None)
            keyword_two = request.GET.get('keyword_two', None)
            selected_column_one = request.GET.get('selected_column_one', None)
            selected_column_two = request.GET.get('selected_column_two', None)
            year = request.GET.get('year', "")
            date_number_no_one = request.GET.get('date_number_no_one', "")

            # return JsonResponse({'success': True, 'id': service.id, 'color': service.color})
            user = request.user

            return await skeleton(request, user, date_number_no_one, year, keyword_one, keyword_two, selected_column_one, selected_column_two, page)
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
            execution_contract_plan = request.POST['execution_contract_plan']
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
            execution_contract_fact = request.POST['execution_contract_fact']
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
            execution = request.POST['execution']
            contract_balance = request.POST['contract_balance']
            color = request.POST.get('color')

            # if certificate == '0' and certificate_no == '0':
            #     color = '#dff0d8'

            if way == 'п.4 ч.1 ст.93':

                # Найдите запись по ID и обновите цвет
                ServicesVault_ = await sync_to_async(ServicesVault.objects.get)(KOSGU=KOSGU)

                # ServicesVault.DopFC = 'DopFC'
                # ServicesVault.budget_limit = 'budget_limit'
                # ServicesVault.off_budget_limit = 'off_budget_limit'
                # ServicesVault.budget_planned = 'budget_planned'
                # ServicesVault.off_budget_planned = 'off_budget_planned'
                ServicesVault_.budget_concluded = contract_price
                # ServicesVault.off_budget_concluded = 'off_budget_concluded'
                # ServicesVault.budget_completed = 'budget_completed'
                # ServicesVault.off_budget_completed = 'off_budget_completed'
                # ServicesVault.budget_execution = 'budget_execution'
                # ServicesVault.off_budget_execution = 'off_budget_execution'
                # ServicesVault.budget_remainder = 'budget_remainder'
                # ServicesVault.off_budget_remainder = 'off_budget_remainder'
                # ServicesVault.budget_plans = 'budget_plans'
                # ServicesVault.off_budget_plans = 'off_budget_plans'

                await sync_to_async(ServicesVault_.save)()

            # Получаем следующий ID
            latest_service = await sync_to_async(Services.objects.order_by('-id_id').first)()
            try:
                id_id = (int(latest_service.id_id) + 1) if latest_service and latest_service.id_id.isdigit() else 1
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

            user = request.user

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

            return await skeleton(request, user, contract_date, end_date, keyword_one, keyword_two, selected_column_one, selected_column_two, page, KOSGU_user, keyword_one_user, keyword_two_user, selected_column_one_user, selected_column_two_user, page_user)
        except Services.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Service not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON.'}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)