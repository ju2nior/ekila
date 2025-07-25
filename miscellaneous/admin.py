from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from miscellaneous.forms import AboutAdminForm
from miscellaneous.forms import VideoAdminForm
from miscellaneous.models import About
from miscellaneous.models import Cookie
from miscellaneous.models import GeneralCondition
from miscellaneous.models import LegalNotice
from miscellaneous.models import PersonalData
from miscellaneous.models import Publicity
from miscellaneous.models import Service
from miscellaneous.models import Slider
from miscellaneous.models import Video


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ("title",)
    form = AboutAdminForm

    class Media:
        js = ("js/tiny.js",)
        css = {"all": ("css/custom_admin.css",)}


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    form = VideoAdminForm
    list_display = ("title", "category", "created_at")
    list_filter = ("category",)
    search_fields = ("title", "category")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by("-created_at")

    class Media:
        js = ("js/tiny.js",)
        css = {"all": ("css/custom_admin.css",)}


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "url",
        "created_at",
        "end_date",
        "draft",
        "is_welcome",
        "slider_image",
    )
    list_filter = ("draft", "is_welcome")
    actions = ["make_welcome_slider"]

    def slider_image(self, obj):
        return format_html(
            '<img src="{}" style="max-height: 50px; max-width: 100px;" />',
            obj.image.url,
        )

    slider_image.short_description = _("Visualisation de l'image")
    slider_image.allow_tags = True

    def save_model(self, request, obj, form, change):
        if obj.is_welcome:
            other_welcome_sliders = Slider.objects.filter(is_welcome=True)
            if change:
                other_welcome_sliders = other_welcome_sliders.exclude(pk=obj.pk)
            other_welcome_sliders.update(is_welcome=False)
        return super().save_model(request, obj, form, change)

    def make_welcome_slider(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(
                request,
                _("Selectionner un seul carroussel comme celle de bienvenue"),
                level="ERROR",
            )
            return

        Slider.objects.filter(is_welcome=True).update(is_welcome=False)
        queryset.update(is_welcome=True)
        self.message_user(request, _("Modifier avec succès"))

    make_welcome_slider.short_description = _("Marquer comme carroussel de Bienvenue")


admin.site.register(Publicity)
admin.site.register(GeneralCondition)
admin.site.register(LegalNotice)
admin.site.register(PersonalData)
admin.site.register(Cookie)
admin.site.register(Service)
