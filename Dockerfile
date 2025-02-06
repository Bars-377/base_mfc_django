# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Устанавливаем системные зависимости для mysqlclient
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    libmariadb-dev \
    pkg-config \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Копируем файлы проекта в контейнер
COPY . /app

# Устанавливаем зависимости
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# # Копируем директорию виртуального окружения в контейнер
# COPY myenv /app/myenv

# # Устанавливаем переменную окружения для Python, чтобы он использовал библиотеки из виртуального окружения
# ENV VIRTUAL_ENV=/app/myenv
# ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Открываем порт для приложения
EXPOSE 8500

# Копируем entrypoint скрипт
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Устанавливаем entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Команда для запуска приложения
CMD ["sh", "-c", "cd async_mysql_project && uvicorn async_mysql_project.asgi:application --host 0.0.0.0 --port 8500"]
