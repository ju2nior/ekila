from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField


class BaseMiscellaneousModel(models.Model):
    text = models.TextField(blank=True)

    class Meta:
        abstract = True

    def clean(self):
        if not self.pk and self.__class__.objects.exists():
            raise ValidationError(
                _(
                    "Only one instance of %(model_name)s is allowed. Please update the existing instance."
                ),
                params={"model_name": self._meta.verbose_name},
            )


class About(BaseMiscellaneousModel):
    title = models.CharField(
        _("Titre de la section à propos"),
        max_length=100,
        blank=True,
    )
    text = RichTextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = _("À propos")
        verbose_name = _("A propos")

    def __str__(self):
        return "Texte à propos"


class Cookie(BaseMiscellaneousModel):
    class Meta:
        verbose_name_plural = _("Les Cookies")
        verbose_name = _("Cookie")

    def __str__(self):
        return "Texte des cookies du site"


class PersonalData(BaseMiscellaneousModel):
    class Meta:
        verbose_name_plural = _("Texte sur les données personnelles")
        verbose_name = _("Donnée personnelle")

    def __str__(self):
        return "Texte sur les données personnelles"


class LegalNotice(BaseMiscellaneousModel):
    class Meta:
        verbose_name_plural = _("Texte sur les mentions légales")
        verbose_name = _("Mention légale")

    def __str__(self):
        return "Texte sur les mentions légales"


class GeneralCondition(BaseMiscellaneousModel):
    class Meta:
        verbose_name_plural = _("Texte sur les conditions générales")
        verbose_name = _("Conditions générales")

    def __str__(self):
        return "Texte sur les CGU"


class Publicity(models.Model):
    pub_file = models.FileField(upload_to="images/", blank=True)
    pub_link = models.URLField(blank=True)

    class Meta:
        verbose_name_plural = _("Les Publicités")
        verbose_name = _("Publicités")


class Slider(models.Model):
    title = models.CharField(_("Titre du carroussel"), max_length=200, blank=True)
    image = models.ImageField(
        _("Image du carroussel"), upload_to="images/", blank=False
    )
    url = models.URLField(_("Lien du carroussel pour la pub"), blank=True)
    created_at = models.DateField(_("Date de debut"), editable=True)
    end_date = models.DateField(_("Date de fin"), editable=True)
    draft = models.BooleanField(_("Est en brouillard ?"), default=False)
    is_welcome = models.BooleanField(_("Carroussel de bienvenue ?"), default=False)
    description = RichTextField(blank=True, null=True)

    class Meta:
        ordering = ["created_at"]
        verbose_name_plural = _("Les carrouselles")
        verbose_name = _("Carrouselles")

    def __str__(self) -> str:
        return self.title

    def clean(self):
        if self.end_date < self.created_at:
            raise ValidationError(
                _("La date de fin doit être postérieure à la date de début.")
            )
        if (
            self.is_welcome
            and Slider.objects.filter(is_welcome=True).exclude(pk=self.pk).exists()
        ):
            raise ValidationError(
                _("Il n'est possible que d'avoir un seul carroussel de bienvenue")
            )


class Video(models.Model):
    title = models.CharField(max_length=50, verbose_name=_("Titre de la vidéo"))
    category = models.CharField(max_length=200, default="", verbose_name=_("Catégorie"))
    video_file = models.FileField(
        upload_to="videos/",
        verbose_name=_("Fichier vidéo"),
        blank=True,
        help_text=_("Fichier vidéo"),
    )
    video_url = models.URLField(
        blank=True,
        verbose_name=_("URL de la vidéo"),
        help_text=_("URL de la vidéo Youtube ou Vimeo"),
    )
    description = RichTextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True, verbose_name=_("Date d'ajout"))
    slug = models.SlugField(unique=True, blank=True, verbose_name=_("Slug"))

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = _("Les vidéos")
        verbose_name = _("Vidéo")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


class Service(models.Model):
    name = models.CharField(_("Service name"), max_length=100)
    email = models.EmailField(_("Service email"))

    def __str__(self):
        return self.name
