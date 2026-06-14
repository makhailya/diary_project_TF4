from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import (
    ListView, DetailView,
    CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy

from .models import Entry
from .forms import EntryForm
from .mixins import EntryOwnerMixin


class EntryListView(LoginRequiredMixin, ListView):
    model = Entry
    template_name = 'diary/entry_list.html'
    context_object_name = 'entries'
    paginate_by = 10

    def get_queryset(self):
        return Entry.objects.filter(
            author=self.request.user
        ).order_by('-created_at')


class EntryDetailView(EntryOwnerMixin, DetailView):
    model = Entry
    template_name = 'diary/entry_detail.html'
    context_object_name = 'entry'


class EntryCreateView(LoginRequiredMixin, CreateView):
    model = Entry
    form_class = EntryForm
    template_name = 'diary/entry_form.html'
    success_url = reverse_lazy('diary:entry_list')

    def form_valid(self, form):
        entry = form.save(commit=False)
        entry.author = self.request.user
        entry.save()

        messages.success(self.request, 'Запись успешно создана! ✍️')
        return redirect(self.success_url)


class EntryUpdateView(EntryOwnerMixin, UpdateView):
    model = Entry
    form_class = EntryForm
    template_name = 'diary/entry_form.html'

    def get_success_url(self):
        return reverse_lazy(
            'diary:entry_detail', kwargs={'pk': self.object.pk}
        )

    def form_valid(self, form):
        messages.success(self.request, 'Запись обновлена! ✅')
        return super().form_valid(form)


class EntryDeleteView(EntryOwnerMixin, DeleteView):
    model = Entry
    template_name = 'diary/entry_confirm_delete.html'
    success_url = reverse_lazy('diary:entry_list')

    def form_valid(self, form):
        messages.success(self.request, 'Запись удалена 🗑️')
        return super().form_valid(form)
