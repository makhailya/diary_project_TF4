from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class Entry(models.Model):
    MOOD_CHOICES = [
        ('great', '😄 Отлично'),
        ('good', '🙂 Хорошо'),
        ('neutral', '😐 Нейтрально'),
        ('bad', '😔 Плохо'),
        ('terrible', '😢 Ужасно'),
    ]

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='entries',
        verbose_name='Автор'
    )

    title = models.CharField(
        max_length=200,
        verbose_name='Заголовок'
    )

    content = models.TextField(
        verbose_name='Содержание'
    )

    mood = models.CharField(
        max_length=10,
        choices=MOOD_CHOICES,
        default='neutral',
        verbose_name='Настроение'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def __str__(self):
        author: AbstractUser = self.author
        return f'{self.title} — {author.username}'

    def get_mood_display_emoji(self):
        mood_map = {
            'great': '😄',
            'good': '🙂',
            'neutral': '😐',
            'bad': '😔',
            'terrible': '😢',
        }
        return mood_map.get(self.mood, '😐')
