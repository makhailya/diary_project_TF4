from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class EntryOwnerMixin(LoginRequiredMixin):
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.author != self.request.user:
            raise PermissionDenied(
                "У вас нет доступа к этой записи."
            )

        return obj
