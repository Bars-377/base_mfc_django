from django.contrib import admin
from .models import UserActionLog
from datetime import timedelta

@admin.register(UserActionLog)
class UserActionLogAdmin(admin.ModelAdmin):
    list_display = ('formatted_timestamp', 'username', 'action')
    ordering = ('-timestamp',)
    search_fields = ('username', 'action')

    def formatted_timestamp(self, obj):
        # Добавляем 7 часов к timestamp
        adjusted_time = obj.timestamp + timedelta(hours=7)
        return adjusted_time.strftime('%Y-%m-%d %H:%M')  # Форматируем дату и время

    def has_change_permission(self, request, obj=None):
        # Запрещаем редактирование
        return False

from .models import UserActionLog, Services  # Импортируем модель Services
from django.utils.html import format_html

@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('id_id',)
    search_fields = ('name',)

    def get_queryset(self, request):
        """Настройка выборки данных, если необходимо"""
        return super().get_queryset(request)

    def has_change_permission(self, request, obj=None):
        # Запрещаем редактирование
        return False

from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from asgiref.sync import sync_to_async

from urllib.parse import urlencode
from django.http import HttpResponseRedirect

def group_required(*group_names):
    def decorator(view_func):
        async def _wrapped_view(request, *args, **kwargs):
            user_groups = await sync_to_async(lambda: list(request.user.groups.values_list('name', flat=True)), thread_sensitive=True)()
            if not any(group in user_groups for group in group_names):
                await sync_to_async(messages.error)(request, "У вас недостаточно прав для этого действия!")

                # scroll_position = request.GET.get('scroll_position')

                # print('params', request.GET)

                # # Формируем URL с query-параметрами
                # redirect_url = f"{reverse('data_table_view')}?scroll_position={scroll_position}"

                params = request.GET.copy()  # копируем QueryDict, чтобы не изменять оригинал

                redirect_url = f"{reverse('data_table_view')}?{urlencode(params)}"

                # Перенаправляем пользователя
                return HttpResponseRedirect(redirect_url)

                # return redirect(reverse('data_table_view'))
            return await view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
