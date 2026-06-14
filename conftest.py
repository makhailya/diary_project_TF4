import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

from diary.models import Entry

User = get_user_model()


@pytest.fixture
def user(db) -> AbstractUser:
    _ = db
    return User.objects.create_user(  # type: ignore[attr-defined]
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )


@pytest.fixture
def another_user(db) -> AbstractUser:
    _ = db
    return User.objects.create_user(  # type: ignore[attr-defined]
        username='anotheruser',
        email='another@example.com',
        password='testpass123'
    )


@pytest.fixture
def authenticated_client(client, user):
    client.login(username='testuser', password='testpass123')
    return client


@pytest.fixture
def entry(db, user) -> Entry:
    _ = db
    return Entry.objects.create(
        author=user,
        title='Тестовая запись',
        content='Тестовое содержание записи дневника.',
        mood='good'
    )
