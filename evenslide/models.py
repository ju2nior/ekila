from django.db import models
from ulid import ulid
from django.utils.translation import gettext_lazy as _
from django.template.context_processors import media
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField


def media(instance, filename):
    return f"evenements/{instance.id}/{filename}"

def ulid():

    import uuid
    return str(uuid.uuid4())

class Action(models.Model):
    id = models.CharField(primary_key=True, max_length=30, default=ulid, editable=False, db_index=True)
    nom = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nom

class TypeEvenement(models.Model):
    id = models.CharField(primary_key=True, max_length=30, default=ulid, editable=False, db_index=True)
    nom = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nom

class Evenement(models.Model):
    id = models.CharField(primary_key=True, max_length=30, default=ulid, editable=False, db_index=True)
    title = models.CharField(max_length=128)
    intitule = models.CharField(max_length=300)
    localisation = models.CharField(max_length=30)
    image = models.ImageField(upload_to=media, blank=True, null=True)
    heur = models.TimeField()
    type = models.ForeignKey(TypeEvenement, on_delete=models.SET_NULL, null=True, blank=True)
    prix = models.PositiveIntegerField(blank=True, default=0)
    nb_place = models.PositiveIntegerField(blank=True, null=True, default=0)
    nb_tickets = models.PositiveIntegerField(default=0, blank=True, null=True)
    actions = models.ForeignKey(Action, on_delete=models.SET_NULL, null=True, blank=True)
    detail = RichTextField(blank=True, null=True)


    def reserver_ticket(self):
        if self.nb_tickets >= self.nb_place:
            raise ValidationError("Plus de places disponibles.")
        self.nb_tickets += 1
        self.save()

    def places_restantes(self):
        return self.nb_place - self.nb_tickets

    def __str__(self):
        return f"{self.title} ({self.nb_tickets}/{self.nb_place} tickets réservés)"


# =================



