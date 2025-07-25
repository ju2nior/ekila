from django import forms
from .models import *

class EvenementForm(forms.ModelForm):
    class Meta:
        model = Evenement
        fields = ['title', 'intitule', 'localisation', 'heur', 'type', 'prix', 'nb_place', 'nb_tickets', 'actions', 'detail'] 

class ActionForm(forms.ModelForm):
    class Meta:
        model = Action
        fields = ['nom']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de l’action'}),
        }

class TypeForm(forms.ModelForm):
    class Meta:
        model = TypeEvenement 
        fields = ['nom']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du type'}),
        }