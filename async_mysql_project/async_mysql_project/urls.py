"""
URL configuration for async_mysql_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from data_app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

from django.contrib import admin

urlpatterns = [
    path('accounts/login/', views.login_view, name='login'),  # Ваше представление для входа
    path('accounts/register/', views.register_view, name='register'),  # Ваше представление для регистрации
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('', views.data_table_view, name='data_table_view'),
    path('update_color/<int:row_id>/', views.update_color, name='update_color'),
    path('update_color_user/<int:row_id>/', views.update_color_user, name='update_color_user'),
    path('update_color_user_two/<int:row_id>/', views.update_color_user_two, name='update_color_user_two'),
    path('update_record/<int:row_id>/', views.update_record, name='update_record'),
    path('update_record_user/<int:row_id>/', views.update_record_user, name='update_record_user'),
    path('update_record_user_two/<int:row_id>/', views.update_record_user_two, name='update_record_user_two'),
    path('add_record/', views.add_record, name='add_record'),
    path('add_record_two/', views.add_record_two, name='add_record_two'),
    path('add/', views.add, name='add'),
    path('add_two/', views.add_two, name='add_two'),
    path('edit/<int:row_id>/', views.edit, name='edit'),
    path('edit_user/<int:row_id>/', views.edit_user, name='edit_user'),
    path('edit_user_two/<int:row_id>/', views.edit_user_two, name='edit_user_two'),
    path('delete_record/', views.delete_record, name='delete_record'),
    path('delete_record_two/', views.delete_record_two, name='delete_record_two'),
    path("upload/", views.upload_file, name="upload_file"),
    path("admin/", admin.site.urls),
    path("file/<str:filename>/", views.download_file, name="download_file"),
    path('backup_one/', views.backup_to_backup_one, name='backup_to_backup_one'),
    path('backup_two/', views.backup_to_backup_two, name='backup_to_backup_two'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Эта строка решает проблема поиска статических файлов

# Для доступа к папке static
# static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

