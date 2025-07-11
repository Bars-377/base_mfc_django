"""
ASGI config for async_mysql_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from data_app import routing  # Импортируйте маршруты вашего приложения

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'async_mysql_project.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns  # Укажите маршруты для веб-сокетов
        )
    ),
})