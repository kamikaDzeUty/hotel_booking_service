# Hotel Booking Service 🚀

## 🔧 Стек технологий

* **Django 4.2** — веб-фреймворк на Python
* **Django REST Framework** — построение REST API
* **PostgreSQL** — реляционная база данных
* **Docker & Docker Compose** — контейнеризация и оркестрация
* **Poetry** — управление зависимостями и виртуальным окружением
* **Pydantic Settings** — типизация и конфигурация через env
* **Pytest & pytest-django** — автотесты
* **Pre-commit & Ruff** — статический анализ и форматирование кода

## 🚀 Запуск проекта

### 1. Подготовка переменных окружения

1. Скопируйте шаблон:

   ```bash
   cp .env.example .env
   ```
2. Заполните в `.env`:

   ```dotenv
   DEBUG=True
   SECRET_KEY=ваш_секретный_ключ
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=hotel_booking
   DATABASE_HOST=db
   DATABASE_PORT=5432
   ```

### 2. Локальный запуск (Poetry)

```bash
poetry install
poetry run python manage.py migrate
poetry run python manage.py runserver
```

Приложение доступно по адресу `http://127.0.0.1:8888/`.

### 3. Запуск через Docker Compose

```bash
docker-compose up --build    # сборка образов
docker-compose up -d      # запуск сервисов в фоне
docker-compose logs     # просмотр логов
docker-compose down -v    # остановка и удаление контейнеров и volumes
```

## 🎲 Тестирование

```bash
# локально
poetry run pytest
# внутри Docker
docker-compose exec web pytest
```

## 🔍 Линтинг и форматирование

```bash
ruff check --fix   # ruff + auto-fixes
```

## 📡 API Endpoints

### Комнаты

* `GET    /api/rooms/?ordering=price_per_night` — список комнат, сортировка по цене (asc/desc)
* `POST   /api/rooms/` — создать комнату
* `GET    /api/rooms/{id}/` — получить конкретную комнату
* `PUT    /api/rooms/{id}/` — полное обновление
* `PATCH  /api/rooms/{id}/` — частичное обновление
* `DELETE /api/rooms/{id}/` — удалить комнату

### Брони

* `GET    /api/bookings/?room={room_id}` — список броней по комнате, сортировка по дате заезда
* `POST   /api/bookings/` — создать бронь
* `GET    /api/bookings/{id}/` — получить бронь
* `PUT    /api/bookings/{id}/` — полное обновление
* `PATCH  /api/bookings/{id}/` — смена статуса
* `DELETE /api/bookings/{id}/` — удалить бронь
