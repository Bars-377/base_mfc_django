from django.urls import re_path
from .consumers import ExportConsumer

websocket_urlpatterns = [
    re_path(r'ws/some_path/', ExportConsumer.as_asgi()),  # Здесь используйте нужный путь
]
