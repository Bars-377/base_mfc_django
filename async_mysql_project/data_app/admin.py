# from django.shortcuts import redirect
# from django.urls import reverse
# from django.contrib import messages
# from asgiref.sync import sync_to_async

# def admin_required(view_func):
#     async def _wrapped_view(request, *args, **kwargs):
#         is_superuser = await sync_to_async(lambda: request.user.is_superuser, thread_sensitive=True)()
#         if not is_superuser:
#             await sync_to_async(messages.error)(request, "Редактировать таблицу Закупки может только Администратор")
#             return redirect(reverse('data_table_view'))
#         return await view_func(request, *args, **kwargs)

#     return _wrapped_view

from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from asgiref.sync import sync_to_async

def group_required(*group_names):
    def decorator(view_func):
        async def _wrapped_view(request, *args, **kwargs):
            user_groups = await sync_to_async(lambda: list(request.user.groups.values_list('name', flat=True)), thread_sensitive=True)()
            if not any(group in user_groups for group in group_names):
                await sync_to_async(messages.error)(request, "У вас недостаточно прав для редактирования")
                return redirect(reverse('data_table_view'))
            return await view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
