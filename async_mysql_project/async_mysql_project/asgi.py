"""
ASGI config for async_mysql_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'async_mysql_project.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # если нужно, можно добавить WebSockets или другие протоколы
})