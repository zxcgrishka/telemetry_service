# Сервис Телеметрии

RESTful API сервис для сбора телеметрических данных с устройств и асинхронной обработки аналитики.

## Технологический стек
- **Фреймворк:** FastAPI
- **База данных:** PostgreSQL
- **Очередь задач:** Celery + Redis
- **Контейнеризация:** Docker и Docker Compose
- **Нагрузочное тестирование:** Locust

## Структура проекта
- `app/`: Основной код приложения
  - `main.py`: Точка входа FastAPI
  - `models.py`: Модели базы данных SQLAlchemy
  - `schemas.py`: Схемы данных Pydantic (валидация)
  - `crud.py`: Операции с базой данных
  - `worker.py`: Конфигурация и задачи Celery
  - `routers/`: API эндпоинты, сгруппированные по ресурсам
- `alembic/`: Миграции базы данных
- `Dockerfile` и `docker-compose.yml`: Настройки контейнеризации
- `locustfile.py`: Сценарий нагрузочного тестирования

## Как запустить

### Использование Docker (Рекомендуется)
1. Убедитесь, что у вас установлены и запущены Docker и Docker Compose.
2. Выполните следующую команду:
   ```bash
   docker-compose up --build -d
   ```
3. API будет доступно по адресу `http://localhost:8080`.
4. Интерактивная документация API (Swagger UI) доступна по адресу `http://localhost:8080/docs`.

### Локальная разработка (без Docker)
1. Установите зависимости с помощью Poetry:
   ```bash
   poetry install
   ```
2. Поднимите локально PostgreSQL и Redis.
3. Настройте переменные окружения (создайте файл `.env` или экспортируйте их):
   ```
   DATABASE_URL=postgresql+asyncpg://user:pass@localhost/telemetry
   SYNC_DATABASE_URL=postgresql://user:pass@localhost/telemetry
   REDIS_URL=redis://localhost:6379/0
   ```
4. Примените миграции базы данных:
   ```bash
   poetry run alembic upgrade head
   ```
5. Запустите сервер FastAPI:
   ```bash
   poetry run uvicorn app.main:app --reload --port 8080
   ```
6. Запустите воркер Celery:
   ```bash
   poetry run celery -A app.worker.celery worker --loglevel=info
   ```

## API Эндпоинты

### Пользователи и Устройства
- `POST /users/`: Создать нового пользователя.
- `POST /devices/`: Зарегистрировать устройство и привязать его к пользователю.

### Сбор телеметрии
- `POST /telemetry/{device_id}`: Получить данные телеметрии (`x`, `y`, `z`).

### Аналитика
- `POST /analytics/device/{device_id}`: Запустить анализ для конкретного устройства (опциональные параметры `start_time`, `end_time`). Возвращает `task_id`.
- `POST /analytics/user/{user_id}`: Запустить анализ для всех устройств пользователя. Возвращает `task_id`.
- `GET /analytics/task/{task_id}`: Проверить статус задачи и получить результаты (минимум, максимум, количество, сумма, медиана).

## Нагрузочное тестирование
Чтобы запустить нагрузочные тесты с помощью Locust:
1. Убедитесь, что сервис запущен.
2. Запустите Locust:
   ```bash
   poetry run locust
   ```
3. Откройте `http://localhost:8089` в браузере и запустите тест.
