from django.shortcuts import redirect
from django.urls import reverse

from django.contrib import messages  # Импортируем messages

def admin_required(view_func):
    """
    Декоратор для проверки, является ли пользователь администратором (superuser).
    Если нет — редирект на страницу data_table_view.
    """
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser == 2:
            messages.error(request, "Редактировать таблицу Закупки может только Администратор")
            return redirect(reverse('data_table_view'))  # Перенаправляем на data_table_view

        print('POPAL')
        return view_func(request, *args, **kwargs)

    return _wrapped_view