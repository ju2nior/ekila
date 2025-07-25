# actuality/admin.py

from django.contrib import admin
from actuality.forms import ActualityAdminForm
from actuality.models import Actuality


@admin.register(Actuality)
class ActualiteAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "created_at", "is_up_to_date")
    list_filter = ("created_at", "category", "username")
    search_fields = ("title", "category")
    list_per_page = 30
    form = ActualityAdminForm  # ← CKEditor + Placeholder

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        user = request.user
        if not user.is_superuser:
            return queryset.filter(user=user.username)
        return queryset

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user.get_username()
        super().save_model(request, obj, form, change)
