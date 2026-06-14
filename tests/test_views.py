import pytest
from django.urls import reverse
from diary.models import Entry


@pytest.mark.django_db
class TestEntryListView:
    def test_list_requires_login(self, client):
        url = reverse('diary:entry_list')
        response = client.get(url)
        assert response.status_code == 302
        assert '/users/login/' in response.url

    def test_list_shows_only_own_entries(
        self, authenticated_client, entry, another_user
    ):
        other_entry = Entry.objects.create(
            author=another_user,
            title='Чужая запись',
            content='Это чужой дневник'
        )
        url = reverse('diary:entry_list')
        response = authenticated_client.get(url)

        assert response.status_code == 200
        entries = response.context['entries']

        assert entry in entries
        assert other_entry not in entries


@pytest.mark.django_db
class TestEntryDetailView:
    def test_owner_can_view_entry(self, authenticated_client, entry):
        url = reverse('diary:entry_detail', kwargs={'pk': entry.pk})
        response = authenticated_client.get(url)
        assert response.status_code == 200

    def test_other_user_cannot_view_entry(self, client, entry, another_user):
        client.login(username='anotheruser', password='testpass123')
        url = reverse('diary:entry_detail', kwargs={'pk': entry.pk})
        response = client.get(url)
        assert response.status_code == 403

    def test_unauthenticated_cannot_view_entry(self, client, entry):
        url = reverse('diary:entry_detail', kwargs={'pk': entry.pk})
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestEntryCreateView:
    def test_create_entry_successfully(self, authenticated_client, user):
        url = reverse('diary:entry_create')
        data = {
            'title': 'Новая запись',
            'content': 'Содержание новой записи',
            'mood': 'good'
        }
        response = authenticated_client.post(url, data)

        assert response.status_code == 302
        assert Entry.objects.filter(title='Новая запись').exists()

    def test_entry_author_set_automatically(self, authenticated_client, user):
        url = reverse('diary:entry_create')
        data = {
            'title': 'Автоматический автор',
            'content': 'Проверка автора',
            'mood': 'neutral'
        }
        authenticated_client.post(url, data)
        entry = Entry.objects.get(title='Автоматический автор')
        assert entry.author == user

    def test_unauthenticated_cannot_create(self, client):
        url = reverse('diary:entry_create')
        response = client.post(url, {
            'title': 'Взлом', 'content': '...', 'mood': 'good'
        })
        assert response.status_code == 302
        assert not Entry.objects.filter(title='Взлом').exists()


@pytest.mark.django_db
class TestEntryUpdateView:
    def test_owner_can_update_entry(self, authenticated_client, entry):
        url = reverse('diary:entry_update', kwargs={'pk': entry.pk})
        data = {
            'title': 'Обновлённый заголовок',
            'content': 'Обновлённое содержание',
            'mood': 'great'
        }
        response = authenticated_client.post(url, data)
        assert response.status_code == 302

        entry.refresh_from_db()
        assert entry.title == 'Обновлённый заголовок'
        assert entry.mood == 'great'

    def test_other_user_cannot_update_entry(self, client, entry, another_user):
        client.login(username='anotheruser', password='testpass123')
        url = reverse('diary:entry_update', kwargs={'pk': entry.pk})
        response = client.post(url, {
            'title': 'Взлом!', 'content': '...', 'mood': 'good'
        })
        assert response.status_code == 403
        entry.refresh_from_db()
        assert entry.title == 'Тестовая запись'


@pytest.mark.django_db
class TestEntryDeleteView:
    def test_owner_can_delete_entry(self, authenticated_client, entry):
        url = reverse('diary:entry_delete', kwargs={'pk': entry.pk})
        response = authenticated_client.post(url)
        assert response.status_code == 302
        assert not Entry.objects.filter(pk=entry.pk).exists()

    def test_other_user_cannot_delete_entry(self, client, entry, another_user):
        client.login(username='anotheruser', password='testpass123')
        url = reverse('diary:entry_delete', kwargs={'pk': entry.pk})
        response = client.post(url)
        assert response.status_code == 403
        assert Entry.objects.filter(pk=entry.pk).exists()
