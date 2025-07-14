async def format_number(value):
    """Форматируем число"""
    if isinstance(value, (int, float)):
        number_final = float(value)
    elif value is None or not value or str(value).strip() == '' or str(value) == 'None':
        number_final = 0.00
    else:
        try:
            # Удаляем пробелы и заменяем запятую на точку
            value_str = str(value).replace(' ', '').replace(',', '.')
            number_final = float(value_str)
        except ValueError:
            # Если преобразование в число не удалось, возвращаем 0.00
            number_final = 0.00
    return number_final

def errors(e):
    """Вывод подробной информации об ошибке"""
    print(f"Поймано исключение: {type(e).__name__}")
    print(f"Сообщение об ошибке: {str(e)}")
    import traceback
    print("Трассировка стека (stack trace):")
    traceback.print_exc()

from asgiref.sync import sync_to_async
from .models import UserActionLog

@sync_to_async
def log_user_action(user, action):
    # Сохраняем лог в базу данных
    UserActionLog.objects.create(username=user.username, action=action)