import pytest
from diary.forms import EntryForm


@pytest.mark.django_db
class TestEntryForm:
    def test_valid_form(self):
        data = {
            'title': 'Мой день',
            'content': 'Сегодня был хороший день.',
            'mood': 'good'
        }
        form = EntryForm(data=data)
        assert form.is_valid()

    def test_form_without_title(self):
        data = {
            'title': '',
            'content': 'Содержание',
            'mood': 'good'
        }
        form = EntryForm(data=data)
        assert not form.is_valid()
        assert 'title' in form.errors

    def test_form_without_content(self):
        data = {
            'title': 'Заголовок',
            'content': '',
            'mood': 'good'
        }
        form = EntryForm(data=data)
        assert not form.is_valid()
        assert 'content' in form.errors

    def test_form_invalid_mood(self):
        data = {
            'title': 'Заголовок',
            'content': 'Содержание',
            'mood': 'amazing'
        }
        form = EntryForm(data=data)
        assert not form.is_valid()
