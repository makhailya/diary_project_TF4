from django import forms
from .models import Entry


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ('title', 'content', 'mood')

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Заголовок записи...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Что произошло сегодня?'
            }),
            'mood': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

        labels = {
            'title': 'Заголовок',
            'content': 'Содержание',
            'mood': 'Настроение',
        }
