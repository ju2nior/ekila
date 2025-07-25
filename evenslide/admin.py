from django.contrib import admin
from .models import Evenement, Action, TypeEvenement

@admin.register(Evenement)
class EvenementAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'nb_place', 'nb_tickets')

@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('nom',)

@admin.register(TypeEvenement)
class TypeEvenementAdmin(admin.ModelAdmin):
    list_display = ('nom',)

