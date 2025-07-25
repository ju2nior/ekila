from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField



class Actuality(models.Model):
    category = models.CharField(_("Catégorie de l'actualité"), max_length=200)
    title = models.CharField(_("Titre de l'actualite"), max_length=200, blank=False)
    source = models.CharField(_("Hauteur"), max_length=255, blank=True)
    intitule = models.CharField(_("entrez les origines de vôtre source "), max_length=200, blank=True)
    image = models.ImageField(
        _("Image de l'actualité"), upload_to="images/", blank=True
    )
    text = RichTextField(_("Description de l'actualité"), blank=True)
    is_up_to_date = models.BooleanField(
        _("Actualité à la une ?"),
        default=False,
    )
    
    type = models.CharField(
        _("Type d'actualité"),
        max_length=100,
        choices=[
            ("Politique", "Politique"),
            ("Économie", "Économie"),
            ("International", "International"),
            ("Société", "Société"),
            ("Santé", "Santé"),
            ("Technologie", "Technologie"),
            ("Environnement", "Environnement"),
            ("Culture", "Culture"),
            ("Sports", "Sports"),
            ("Sciences", "Sciences"),
            ("Éducation", "Éducation"),
            ("Justice", "Justice"),
            ("Evènement", "Évènement"),
            ("Innovation", "Innovation"),
            ("Podcast", "Podcast"),
        ],
        default="Politique",
)
    video_link = models.URLField(_("Vidéo concernant l'actualité"), blank=True)
    created_at = models.DateTimeField(_("Date de création"), auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    slug_uri = models.SlugField(
        _("Url converted ?"),
        max_length=200,
    )
    username = models.CharField(_("Créateur de l'article"), max_length=180, blank=True)
    

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = _("Les actualités")
        verbose_name = _("Actualité")

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs) -> None:
        if not self.slug_uri and self.title:
            self.slug_uri = slugify(self.title)
        super().save(*args, **kwargs)
