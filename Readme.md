# Payment System

Django + DRF сервис для приёма платёжных вебхуков от банка и учёта баланса организаций по ИНН.
Технологии

Django 4

Django REST Framework

MySQL 8

Gunicorn

Docker + Docker Compose

pytest + pytest-django

logging
## Структура
`
app
  backend - Логика: модели, сериализаторы, вьюхи, сервисы
  PaymentSystem - Настройки Django
  tests/  - Тесты pytest
  manage.py
  requirements.txt
  entrypoint.sh
  Dockerfile

mysql
  my.cnf - Конфигурация MySQL

docker-compose.yml

.env - нужно создать ENV-переменные
`
## Установка и запуск

Создайте .env по шаблону: .example_env
# Как поднять всё через Docker:

`docker-compose up --build -d`

Приложение будет доступно на http://localhost:8000

## Тесты

Тесты лежат в app/tests/, использовать можно так:

`docker-compose run web pytest`

Также доступны request тесты по http - лежат в request_test

## API

POST /webhook/

Пример тела запроса:

```
{
"operation_id": "11111111-2222-3333-4444-555555555555",
"amount": 145000,
"payer_inn": "1234567890",
"document_number": "PAY-328",
"document_date": "2024-04-27T21:00:00Z"
}
```
Обрабатывает платёж и обновляет баланс. Повторный operation_id игнорируется — защита от дублей.

> GET /balance/{inn}/

Возвращает текущий баланс по ИНН. Пример ответа:

{
"inn": "7701234567",
"balance": 1000.5
}
## Архитектура

views.py — контроллеры

services.py — бизнес-логика

models.py — Organization и Payment

serializers.py — валидация запроса

tests/ — API-тесты: проверка дубликатов, успешных транзакций и баланса

entrypoint.sh - миграции + запуск
