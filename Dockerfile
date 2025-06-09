# 1. Базовый образ: Python 3.12 slim
FROM python:3.12-slim

# 2. Рабочая директория внутри контейнера
WORKDIR /app

# 3. Копируем только файлы с зависимостями и устанавливаем Poetry + библиотеки
COPY pyproject.toml poetry.lock /app/

RUN pip install --no-cache-dir poetry \
 && poetry config virtualenvs.create false \
 && poetry install --no-root --no-interaction --no-ansi

# 4. Копируем весь остальной код
COPY . /app

# 5. Пробрасываем порт Django dev-сервера
EXPOSE 8000

# 6. Запускаем встроенный runserver для быстрого старта
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
