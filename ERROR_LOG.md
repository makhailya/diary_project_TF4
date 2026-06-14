# Error Log — сборка проекта Personal Diary (TF4)

## 15.06.2026

---

### 1. manage.py отсутствовал

**Ошибка:** `fatal: pathspec 'manage.py' did not match any files`

**Причина:** После пересоздания структуры проекта файл manage.py был удалён.

**Решение:** Создан manage.py заново с правильным `DJANGO_SETTINGS_MODULE = 'config.settings'`.

---

### 2. Отсутствовали __init__.py и apps.py в приложениях diary и users

**Ошибка:** `ModuleNotFoundError`, Django не мог найти приложения.

**Причина:** Директории diary/ и users/ были пусты (без __init__.py).

**Решение:** Созданы:
- `diary/__init__.py`, `diary/apps.py`, `diary/migrations/__init__.py`
- `users/__init__.py`, `users/apps.py`, `users/migrations/__init__.py`

---

### 3. Dependency on app with no migrations: users

**Ошибка:** `ValueError: Dependency on app with no migrations: users`

**Причина:** `AUTH_USER_MODEL = 'users.CustomUser'` требует миграции users до diary.

**Решение:** Миграции созданы в правильном порядке:
```bash
python manage.py makemigrations users
python manage.py makemigrations diary
python manage.py migrate
```

---

### 4. settings_test.py — star import (F403/F405)

**Ошибка:** `F403 'from .settings import *' used; unable to detect undefined names`

**Причина:** Импорт `*` делает анализатор кода слепым к переменным.

**Решение:** settings_test.py переписан с явными импортами и настройками.

---

### 5. Длинные строки в urls.py и views.py (E501)

**Ошибка:** `E501 line too long (> 79 characters)` в flake8.

**Причина:** Стандартный лимит flake8 — 79 символов.

**Решение:**
- Перенесены аргументы .as_view() на новые строки в `diary/urls.py`
- Исправлен `get_success_url` в `diary/views.py`
- Добавлен `.flake8` с `max-line-length = 100` (разумный компромисс)

---

---

### 6. PostgreSQL: role "diary_user" does not exist

**Ошибка:** `FATAL: role "diary_user" does not exist` при `runserver`

**Причина:** В `.env` указан порт 5434, пользователь `diary_user` и БД `diary_db`, но они не были созданы в PostgreSQL.

**Решение:** Созданы через psql:
```bash
psql -h localhost -p 5434 -U postgres -c "CREATE ROLE diary_user WITH LOGIN PASSWORD 'diary_password';"
psql -h localhost -p 5434 -U postgres -c "CREATE DATABASE diary_db OWNER diary_user;"
```

---

### 7. Docker build failed: [tool.poetry] section not found

**Ошибка:** `[tool.poetry] section not found in /app/pyproject.toml`

**Причина:** В Dockerfile указан `poetry==1.7.1`, который не поддерживает PEP 621 формат `[project]` в pyproject.toml. Современный pyproject.toml использует секцию `[project]` вместо `[tool.poetry]`.

**Решение:** Обновлён Dockerfile: `poetry==1.7.1` → `"poetry>=2.0.0"`

---

### 8. Docker warning: "ew2" variable is not set

**Ошибка:** `WARN[0000] The "ew2" variable is not set. Defaulting to a blank string.`

**Причина:** В SECRET_KEY был символ `$` (`hpw$ew2!...`), который Docker Compose интерпретирует как подстановку переменной окружения.

**Решение:** Сгенерирован новый SECRET_KEY из alphanumeric символов (без `$`).

---

### 9. docker-compose.yml: version is obsolete

**Ошибка:** `WARN[0000] ... the attribute 'version' is obsolete, it will be ignored`

**Причина:** `version: '3.9'` в docker-compose.yml устарел в современных версиях Docker Compose.

**Решение:** Удалена строка `version: '3.9'`.

---

### Результат

- ✅ 33/33 тестов пройдено
- ✅ Покрытие кода: 99%
- ✅ flake8 — без ошибок
- ✅ 8 атомарных коммитов
- ✅ PostgreSQL работает на порту 5434
