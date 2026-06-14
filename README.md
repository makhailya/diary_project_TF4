# 📔 Personal Diary — Веб-приложение для ведения личного дневника

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Django](https://img.shields.io/badge/Django-6.0-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED)

## 📋 Описание проекта

Personal Diary — веб-приложение для ведения личного дневника. Каждый пользователь
может регистрироваться, создавать записи, редактировать и удалять их. Все записи
приватны — никто кроме автора не имеет к ним доступа.

## 🎯 Функциональность

- Регистрация и авторизация пользователей
- Создание, просмотр, редактирование и удаление записей
- Настроение для каждой записи (5 вариантов)
- Пагинация списка записей
- Разграничение доступа — только автор видит свои записи
- Адаптивный интерфейс на Bootstrap 5

## 🛠️ Стек технологий

| Компонент       | Технология              |
|-----------------|-------------------------|
| Backend         | Python 3.11, Django 6.0 |
| База данных     | PostgreSQL 15           |
| ORM             | Django ORM              |
| Авторизация     | Django Sessions         |
| Шаблоны         | Django Templates        |
| Контейнеризация | Docker, Docker-Compose  |
| Тесты           | pytest, pytest-django   |
| Зависимости     | Poetry                  |

## 🚀 Быстрый старт

### Локальная разработка

1. Клонируй репозиторий:
```bash
git clone https://github.com/makhailya/diary_project_TF4.git
cd diary_project_TF4
```

2. Создай файл `.env` на основе примера:
```bash
cp .env.example .env
```

3. Установи зависимости:
```bash
poetry install
```

4. Примени миграции:
```bash
poetry run python manage.py migrate
```

5. Запусти сервер:
```bash
poetry run python manage.py runserver
```

### Запуск через Docker

```bash
docker-compose up --build
```

### Создание суперпользователя

```bash
poetry run python manage.py createsuperuser
```

### Запуск тестов

```bash
poetry run pytest --cov=diary --cov=users --cov-report=term-missing
```

## 📁 Структура проекта

```
diary_project/
├── config/          # Настройки Django
├── diary/           # Приложение дневника
├── users/           # Авторизация
├── tests/           # Тесты
├── Dockerfile
├── docker-compose.yml
└── pyproject.toml
```

## 🔐 Безопасность

- Разграничение прав: пользователь видит только свои записи
- CSRF-защита на всех формах
- Пароли хранятся в хешированном виде
- Секреты вынесены в `.env` (не попадают в Git)

## 👨‍💻 Автор

**Илья** — Python Backend Developer
