from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import DataTable
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render
import re

from django.db.models import Sum

def skeleton(request, user, date_number_no_one, year, keyword_one, keyword_two, selected_column_one, selected_column_two, page):
    date_number_no_one = None if date_number_no_one == 'None' else date_number_no_one
    year = None if year == 'None' else year
    keyword_one = None if keyword_one == 'None' else keyword_one
    keyword_two = None if keyword_two == 'None' else keyword_two
    selected_column_one = None if selected_column_one == 'None' else selected_column_one
    selected_column_two = None if selected_column_two == 'None' else selected_column_two

    per_page = 20

    # Регулярные выражения для форматов дат
    pattern_dd_mm_yyyy = r'\b\d{2}\.\d{2}\.\d{4}\b'
    pattern_yyyy_mm_dd = r'\b\d{4}-\d{2}-\d{2}\b'

    # Получаем все уникальные значения year и date_number_no_one
    all_years = DataTable.objects.values('year').distinct()
    all_date_number_no_one = DataTable.objects.values('date_number_no_one').distinct()

    # Сбор уникальных годов из year
    service_years = set()
    empty_found_year = False
    for year_value in all_years:
        year_str = year_value['year']
        if not year_str:
            empty_found_year = True
        matches_dd_mm_yyyy = re.findall(pattern_dd_mm_yyyy, year_str)
        matches_yyyy_mm_dd = re.findall(pattern_yyyy_mm_dd, year_str)
        service_years.update([date_str[-4:] for date_str in matches_dd_mm_yyyy])
        service_years.update([date_str[:4] for date_str in matches_yyyy_mm_dd])

    service_years = sorted({str(int(year)) for year in service_years if year.isdigit()})
    if empty_found_year:
        service_years.insert(0, None)

    # Сбор уникальных годов из date_number_no_one
    service_date_number_no_one = set()
    empty_found_date_number_no_one = False
    for date_value in all_date_number_no_one:
        date_str = date_value['date_number_no_one']
        if not date_str:
            empty_found_date_number_no_one = True
        matches_dd_mm_yyyy = re.findall(pattern_dd_mm_yyyy, date_str)
        matches_yyyy_mm_dd = re.findall(pattern_yyyy_mm_dd, date_str)
        service_date_number_no_one.update([date_str[-4:] for date_str in matches_dd_mm_yyyy])
        service_date_number_no_one.update([date_str[:4] for date_str in matches_yyyy_mm_dd])

    service_date_number_no_one = sorted({str(int(date)) for date in service_date_number_no_one if date.isdigit()})
    if empty_found_date_number_no_one:
        service_date_number_no_one.insert(0, None)

    # Построение запроса
    query = DataTable.objects.all()

    if year == 'No':
        year = None
    if date_number_no_one == 'No':
        date_number_no_one = None

    if year == 'None' and date_number_no_one == 'None':
        query = query.exclude(Q(year__regex=pattern_dd_mm_yyyy) | Q(year__regex=pattern_yyyy_mm_dd) |
                            Q(date_number_no_one__regex=pattern_dd_mm_yyyy) | Q(date_number_no_one__regex=pattern_yyyy_mm_dd))
    elif year == 'None' and date_number_no_one:
        query = query.exclude(Q(year__regex=pattern_dd_mm_yyyy) | Q(year__regex=pattern_yyyy_mm_dd)).filter(date_number_no_one__icontains=date_number_no_one)
    elif year == 'None' and not date_number_no_one:
        query = query.exclude(Q(year__regex=pattern_dd_mm_yyyy) | Q(year__regex=pattern_yyyy_mm_dd))
    elif year and date_number_no_one == 'None':
        query = query.exclude(Q(date_number_no_one__regex=pattern_dd_mm_yyyy) | Q(date_number_no_one__regex=pattern_yyyy_mm_dd)).filter(year__icontains=year)
    elif not year and date_number_no_one == 'None':
        query = query.exclude(Q(date_number_no_one__regex=pattern_dd_mm_yyyy) | Q(date_number_no_one__regex=pattern_yyyy_mm_dd))
    elif year and date_number_no_one:
        query = query.filter(Q(year__icontains=year) | Q(date_number_no_one__icontains=date_number_no_one))
    elif year and not date_number_no_one:
        query = query.filter(year__icontains=year)
    elif not year and date_number_no_one:
        query = query.filter(date_number_no_one__icontains=date_number_no_one)

    if keyword_one:
        if selected_column_one and hasattr(DataTable, selected_column_one):
            query = query.filter(**{selected_column_one + '__icontains': keyword_one})
        else:
            filters = Q()
            for field in DataTable._meta.get_fields():
                filters |= Q(**{field.name + '__icontains': keyword_one})
            query = query.filter(filters)

    if keyword_two:
        if selected_column_two and hasattr(DataTable, selected_column_two):
            query = query.filter(**{selected_column_two + '__icontains': keyword_two})
        else:
            filters = Q()
            for field in DataTable._meta.get_fields():
                filters |= Q(**{field.name + '__icontains': keyword_two})
            query = query.filter(filters)

    # Сортировка
    query = query.order_by('id_id', 'year')

    # Логика подсчета стоимости
    if year == 'None' and date_number_no_one == 'None':
        total_cost_1 = query.exclude(Q(year__regex=pattern_dd_mm_yyyy) | Q(year__regex=pattern_yyyy_mm_dd) |
                                    Q(date_number_no_one__regex=pattern_dd_mm_yyyy) | Q(date_number_no_one__regex=pattern_yyyy_mm_dd)).aggregate(Sum('cost'))['cost__sum'] or 0
        total_cost_2 = query.exclude(Q(year__regex=pattern_dd_mm_yyyy) | Q(year__regex=pattern_yyyy_mm_dd) |
                                    Q(date_number_no_one__regex=pattern_dd_mm_yyyy) | Q(date_number_no_one__regex=pattern_yyyy_mm_dd)).aggregate(Sum('certificate'))['certificate__sum'] or 0
        total_cost_3 = query.exclude(Q(year__regex=pattern_dd_mm_yyyy) | Q(year__regex=pattern_yyyy_mm_dd) |
                                    Q(date_number_no_one__regex=pattern_dd_mm_yyyy) | Q(date_number_no_one__regex=pattern_yyyy_mm_dd)).aggregate(Sum('certificate_no'))['certificate_no__sum'] or 0
    elif year and date_number_no_one:
        total_cost_1 = query.filter(Q(year__icontains=year) | Q(date_number_no_one__icontains=year)).aggregate(Sum('cost'))['cost__sum'] or 0
        total_cost_2 = query.filter(Q(year__icontains=year) | Q(date_number_no_one__icontains=year)).aggregate(Sum('certificate'))['certificate__sum'] or 0
        total_cost_3 = query.filter(Q(year__icontains=year) | Q(date_number_no_one__icontains=year)).aggregate(Sum('certificate_no'))['certificate_no__sum'] or 0
    elif year == 'None' and date_number_no_one != 'None':
        total_cost_1 = query.exclude(Q(year__regex=pattern_dd_mm_yyyy) | Q(year__regex=pattern_yyyy_mm_dd)).aggregate(Sum('cost'))['cost__sum'] or 0
        total_cost_2 = query.exclude(Q(year__regex=pattern_dd_mm_yyyy) | Q(year__regex=pattern_yyyy_mm_dd)).aggregate(Sum('certificate'))['certificate__sum'] or 0
        total_cost_3 = query.exclude(Q(year__regex=pattern_dd_mm_yyyy) | Q(year__regex=pattern_yyyy_mm_dd)).aggregate(Sum('certificate_no'))['certificate_no__sum'] or 0
    elif year and not date_number_no_one:
        total_cost_1 = query.filter(Q(year__icontains=year)).aggregate(Sum('cost'))['cost__sum'] or 0
        total_cost_2 = query.filter(Q(year__icontains=year)).aggregate(Sum('certificate'))['certificate__sum'] or 0
        total_cost_3 = query.filter(Q(year__icontains=year)).aggregate(Sum('certificate_no'))['certificate_no__sum'] or 0
    elif year != 'None' and date_number_no_one == 'None':
        total_cost_1 = query.exclude(Q(date_number_no_one__regex=pattern_dd_mm_yyyy) | Q(date_number_no_one__regex=pattern_yyyy_mm_dd)).aggregate(Sum('cost'))['cost__sum'] or 0
        total_cost_2 = query.exclude(Q(date_number_no_one__regex=pattern_dd_mm_yyyy) | Q(date_number_no_one__regex=pattern_yyyy_mm_dd)).aggregate(Sum('certificate'))['certificate__sum'] or 0
        total_cost_3 = query.exclude(Q(date_number_no_one__regex=pattern_dd_mm_yyyy) | Q(date_number_no_one__regex=pattern_yyyy_mm_dd)).aggregate(Sum('certificate_no'))['certificate_no__sum'] or 0
    elif not year and date_number_no_one:
        total_cost_1 = query.filter(Q(date_number_no_one__icontains=date_number_no_one)).aggregate(Sum('cost'))['cost__sum'] or 0
        total_cost_2 = query.filter(Q(date_number_no_one__icontains=date_number_no_one)).aggregate(Sum('certificate'))['certificate__sum'] or 0
        total_cost_3 = query.filter(Q(date_number_no_one__icontains=date_number_no_one)).aggregate(Sum('certificate_no'))['certificate_no__sum'] or 0
    else:
        total_cost_1 = query.aggregate(Sum('cost'))['cost__sum'] or 0
        total_cost_2 = query.aggregate(Sum('certificate'))['certificate__sum'] or 0
        total_cost_3 = query.aggregate(Sum('certificate_no'))['certificate_no__sum'] or 0

    # Пагинация
    paginator = Paginator(query, per_page)
    services = paginator.get_page(page)

    # Получаем общее количество страниц
    total_pages = paginator.num_pages

    # Определяем максимальное количество кнопок для навигации
    max_page_buttons = 5
    start_page = max(1, page - max_page_buttons // 2)
    end_page = min(total_pages, page + max_page_buttons // 2)

    if end_page - start_page < max_page_buttons - 1:
        if start_page > 1:
            end_page = min(total_pages, end_page + (max_page_buttons - (end_page - start_page)))
        else:
            start_page = max(1, end_page - (max_page_buttons - (end_page - start_page)))

    pages = range(start_page, end_page + 1)  # Создаем диапазон страниц

    # Подготовка контекста для шаблона
    context = {
        'data': services,
        'user': user,
        'pages': pages,
        'total_cost_1': total_cost_1,
        'total_cost_2': total_cost_2,
        'total_cost_3': total_cost_3,
        'selected_year': year,
        'selected_date_number_no_one': date_number_no_one,
        'selected_column_one': selected_column_one,
        'selected_column_two': selected_column_two,
        'keyword_one': keyword_one,
        'keyword_two': keyword_two,
        'page': page,
        'total_pages': total_pages,
        'start_page': start_page,
        'end_page': end_page,
        'service_years': service_years,
        'service_date_number_no_one': service_date_number_no_one
    }

    return render(request, 'data_table.html', context)

@login_required
def data_table_view(request):
    total_pages_full = request.GET.get('total_pages_full', None)

    if total_pages_full:
        per_page = 20
        query = DataTable.objects.all()
        total_services_full = query.count()
        page = (total_services_full + per_page - 1) // per_page
    else:
        page = int(request.GET.get('page', 1))

    date_number_no_one = request.GET.get('date_number_no_one', None)
    year = request.GET.get('year', None)
    keyword_one = request.GET.get('keyword_one', None)
    keyword_two = request.GET.get('keyword_two', None)
    selected_column_one = request.GET.get('selected_column_one', None)
    selected_column_two = request.GET.get('selected_column_two', None)

    user = request.user

    return skeleton(request, user, date_number_no_one, year, keyword_one, keyword_two, selected_column_one, selected_column_two, page)

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User

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

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Регистрация прошла успешно. Вы можете войти.")
            return redirect('login')
        else:
            messages.error(request, "Пароли не совпадают")
    return render(request, 'register.html')  # Ваш шаблон для регистрации

@csrf_exempt  # Необходимо, если вы не используете CSRF-токены
def update_color(request, row_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            color = data.get('color')

            # Найдите запись по ID и обновите цвет
            service = DataTable.objects.get(id=row_id)
            service.color = color
            service.save()

            return JsonResponse({'success': True, 'id': service.id, 'color': service.color})
        except DataTable.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Service not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON.'}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)

@csrf_exempt  # Необходимо, если вы не используете CSRF-токены
def delete_record(request, row_id):
    if request.method == 'POST':
        try:
            # Найдите запись по ID и обновите цвет
            service = DataTable.objects.get(id=row_id)

            # Удаление записи
            service.delete()

            # Сообщение об успешном удалении
            messages.success(request, 'Данные успешно удалены!')

            # Перенаправление на главную страницу
            return redirect('data_table_view')
        except DataTable.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Service not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON.'}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)

# from django.shortcuts import get_object_or_404

@csrf_exempt  # Необходимо, если вы не используете CSRF-токены
def add(request):
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

    return render(request, 'add.html', context)

@csrf_exempt  # Необходимо, если вы не используете CSRF-токены
def edit(request, row_id):
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
    # service = get_object_or_404(DataTable, id=row_id)  # Измените на id_id, если используете поле id_id
    service = DataTable.objects.get(id=row_id)

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

    return render(request, 'edit.html', context)

@csrf_exempt  # Необходимо, если вы не используете CSRF-токены
def update_record(request, row_id):
    print('POPAL')
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
            service = DataTable.objects.get(id=row_id)

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

            service.save()

            messages.success(request, "Редактирование прошло успешно.")

            page = int(request.GET.get('page', 1))
            keyword_one = request.GET.get('keyword_one', None)
            keyword_two = request.GET.get('keyword_two', None)
            selected_column_one = request.GET.get('selected_column_one', None)
            selected_column_two = request.GET.get('selected_column_two', None)
            year = request.GET.get('year', "")
            date_number_no_one = request.GET.get('date_number_no_one', "")

            # return JsonResponse({'success': True, 'id': service.id, 'color': service.color})
            user = request.user

            return skeleton(request, user, date_number_no_one, year, keyword_one, keyword_two, selected_column_one, selected_column_two, page)
        except DataTable.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Service not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON.'}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)

@csrf_exempt  # Необходимо, если вы не используете CSRF-токены
def add_record(request):
    print('POPAL')

    if request.method == 'POST':
        try:
            print('FINAL_1')
            total_pages = int(request.GET.get('total_pages', 1))

            name = request.POST['name']
            snils = request.POST['snils']
            location = request.POST['location']
            address_p = request.POST['address_p']
            address = request.POST['address']
            benefit = request.POST['benefit']
            number = request.POST['number']
            year = request.POST['year']
            cost = request.POST['cost']
            certificate = request.POST['certificate']
            date_number_get = request.POST['date_number_get']
            date_number_cancellation = request.POST['date_number_cancellation']
            date_number_no_one = request.POST['date_number_no_one']
            date_number_no_two = request.POST['date_number_no_two']
            certificate_no = request.POST['certificate_no']
            reason = request.POST['reason']
            track = request.POST['track']
            date_post = request.POST['date_post']
            comment = request.POST['comment']
            color = request.POST.get('color')

            print('FINAL_2')

            if certificate == '0' and certificate_no == '0':
                color = '#dff0d8'

            # Получаем следующий ID
            latest_service = DataTable.objects.order_by('-id_id').first()
            id_id = (int(latest_service.id_id) + 1) if latest_service else 1

            new_service = DataTable(id_id=id_id, name=name, snils=snils, location=location,
                                address_p=address_p, address=address, benefit=benefit,
                                number=number, year=year, cost=cost,
                                certificate=certificate, date_number_get=date_number_get,
                                date_number_cancellation=date_number_cancellation,
                                date_number_no_one=date_number_no_one, date_number_no_two=date_number_no_two, certificate_no=certificate_no,
                                reason=reason, track=track, date_post=date_post, comment=comment, color=color)

            new_service.save()
            messages.success(request, 'Данные успешно добавлены!')

            user = request.user

            year = None
            date_number_no_one = None
            keyword_one = None
            keyword_two = None
            selected_column_one=None
            selected_column_two=None
            page = total_pages

            return skeleton(request, user, date_number_no_one, year, keyword_one, keyword_two, selected_column_one, selected_column_two, page)
        except DataTable.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Service not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON.'}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)