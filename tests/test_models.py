import pytest
from diary.models import Entry


@pytest.mark.django_db
class TestEntryModel:
    def test_entry_creation(self, entry):
        assert entry.title == 'Тестовая запись'
        assert entry.content == 'Тестовое содержание записи дневника.'
        assert entry.mood == 'good'

    def test_entry_str_representation(self, entry, user):
        expected = f'Тестовая запись — {user.username}'
        assert str(entry) == expected

    def test_entry_has_created_at(self, entry):
        assert entry.created_at is not None

    def test_entry_has_updated_at(self, entry):
        assert entry.updated_at is not None

    def test_entry_default_mood(self, user, db):
        entry = Entry.objects.create(
            author=user,
            title='Запись без настроения',
            content='Контент'
        )
        assert entry.mood == 'neutral'

    def test_entry_mood_emoji(self, entry):
        entry.mood = 'great'
        assert entry.get_mood_display_emoji() == '😄'

        entry.mood = 'terrible'
        assert entry.get_mood_display_emoji() == '😢'

    def test_entries_ordered_by_newest_first(self, user, db):
        entry1 = Entry.objects.create(author=user, title='Первая', content='...')
        entry2 = Entry.objects.create(author=user, title='Вторая', content='...')
        entries = Entry.objects.filter(author=user)
        assert entries[0] == entry2
        assert entries[1] == entry1

    def test_entry_belongs_to_user(self, entry, user):
        assert entry.author == user

    def test_entry_deleted_when_user_deleted(self, user, db):
        entry = Entry.objects.create(author=user, title='Запись', content='...')
        entry_id = entry.id
        user.delete()
        assert not Entry.objects.filter(id=entry_id).exists()
