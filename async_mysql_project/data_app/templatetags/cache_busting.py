import os
from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def bust_static(path):
    # Берём путь к первой папке из STATICFILES_DIRS
    static_dirs = settings.STATICFILES_DIRS
    static_root = static_dirs[0] if static_dirs else settings.STATIC_ROOT
    full_path = os.path.join(static_root, path)

    try:
        timestamp = int(os.path.getmtime(full_path))
        return f"{settings.STATIC_URL}{path}?v={timestamp}"
    except FileNotFoundError:
        return f"{settings.STATIC_URL}{path}"
