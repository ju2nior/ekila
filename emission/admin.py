from django.contrib import admin

from emission.models import Emission
from emission.models import FridayEditorial
from emission.models import Poadcast
from emission.models import SubEmission


@admin.register(Emission)
class EmissionAdmin(admin.ModelAdmin):
    list_per_page = 20

    list_display = ("title", "presentator", "created_at")
    list_filter = ("created_at", "presentator")
    search_fields = ("title__startswith",)

    class Media:
        js = ("js/tiny.js",)


@admin.register(SubEmission)
class SubEmissionAdmin(admin.ModelAdmin):
    list_per_page = 20

    list_display = ("title", "presentator", "created_at", "emission")
    list_filter = ("created_at", "presentator", "emission")
    search_fields = ("emission",)

    class Media:
        js = ("js/tiny.js",)


@admin.register(FridayEditorial)
class EditoAdmin(admin.ModelAdmin):
    list_per_page = 20

    list_display = ("title", "presentator")
    list_filter = ("created_at", "presentator")
    search_fields = ("title__startswith",)

    class Media:
        js = ("js/tiny.js",)


@admin.register(Poadcast)
class PoadcastAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ("title", "created_at")
    list_filter = ("created_at",)
    search_fields = ("title__icontains",)

    class Media:
        js = ("js/tiny.js",)
