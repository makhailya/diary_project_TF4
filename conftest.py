import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )


@pytest.fixture
def another_user(db):
    return User.objects.create_user(
        username='anotheruser',
        email='another@example.com',
        password='testpass123'
    )


@pytest.fixture
def authenticated_client(client, user):
    client.login(username='testuser', password='testpass123')
    return client


@pytest.fixture
def entry(db, user):
    from diary.models import Entry
    return Entry.objects.create(
        author=user,
        title='Тестовая запись',
        content='Тестовое содержание записи дневника.',
        mood='good'
    )
