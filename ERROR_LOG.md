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

### Результат

- ✅ 33/33 тестов пройдено
- ✅ Покрытие кода: 99%
- ✅ flake8 — без ошибок
- ✅ 8 атомарных коммитов
