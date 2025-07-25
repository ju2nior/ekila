from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField

class BaseEmissionModel(models.Model):
    title = models.CharField(_("Titre de l'emission"), max_length=200, blank=False)
    image = models.ImageField(_("Image de l'emission"), upload_to="images/", blank=True)
    presentator = models.CharField(max_length=200, blank=True)
    description = RichTextField(blank=True, null=True)
    created_at = models.DateTimeField(_("Date de création"), auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    draft = models.BooleanField(_("Brouillon"), default=False)
    slug_uri = models.SlugField(
        _("Url converted ?"),
        max_length=200,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs) -> None:
        if not self.slug_uri and self.title:
            self.slug_uri = slugify(self.title)
        super().save(*args, **kwargs)


class Emission(BaseEmissionModel):
    class Meta:
        ordering = ["created_at"]
        verbose_name_plural = _("Les émissions")
        verbose_name = _("Emission")


class SubEmission(BaseEmissionModel):
    emission = models.ForeignKey(
        Emission, on_delete=models.CASCADE, related_name="sousEmission"
    )
    video_link = models.URLField(blank=True)

    class Meta:
        ordering = ["created_at"]
        verbose_name_plural = _("Les sous emissions")
        verbose_name = _("Sous emission")


class FridayEditorial(models.Model):
    title = models.CharField(_("Titre de l'edito"), max_length=200)
    image = models.FileField(upload_to="images/")
    presentator = models.CharField(_("Nom du presentateur"), max_length=200, blank=True)
    complete_description = RichTextField(blank=True, null=True)
    incomplete_description = RichTextField(blank=True, null=True)
    audio_url = models.URLField(_("Url du fichier audio"), max_length=500, blank=True)
    complete_audio_file = models.FileField(
        _("Fichier audio complet"), upload_to="images/", blank=True
    )
    incomplete_audio_file = models.FileField(
        _("Fichier audio incomplet"), upload_to="images/", blank=True
    )
    created_at = models.DateField(auto_now=True)
    dateline = models.DateField()
    video_link = models.URLField(_("Lien de la video youtube"), blank=True)
    slug_uri = models.SlugField(
        _("Url converted ?"),
        max_length=200,
    )

    class Meta:
        ordering = ["created_at"]
        verbose_name_plural = _("Les editos du vendredi")
        verbose_name = _("Edito")

    def save(self, *args, **kwargs) -> None:
        if not self.slug_uri and self.title:
            self.slug_uri = slugify(self.title)
        super().save(*args, **kwargs)

    def is_still_available(self):
        return (self.dateline - self.created_at).days


class Poadcast(models.Model):
    title = models.CharField(_("Titre du poadcast"), max_length=200)
    image = models.FileField(upload_to="poadcast/images/", blank=True)
    audio = models.FileField(upload_to="poadcast/audio/", blank=False)
    created_at = models.DateField(auto_now=True)
    audio_url = models.URLField(blank=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title
