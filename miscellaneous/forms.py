from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _

from miscellaneous.models import About
from miscellaneous.models import Video


class AboutAdminForm(forms.ModelForm):
    text = forms.CharField(
        label=_("Texte à propos"),
        widget=forms.Textarea(
            attrs={
                "rows": 15,
                "cols": 130,
                "placeholder": _("Saisir votre contenu"),
            }
        ),
        required=True,
    )

    class Meta:
        model = About
        fields = ("title", "text")


class ContactForm(forms.Form):
    email = forms.EmailField()
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self) -> int:
        return send_mail(
            subject=self.cleaned_data["subject"],
            message=self.cleaned_data["message"],
            from_email=self.cleaned_data["email"],
            recipient_list=[settings.MAIL_TO],
            fail_silently=False,
        )

    def clean(self) -> dict[str, str]:
        cleaned_data = super().clean()
        subject = cleaned_data.get("subject")
        message = cleaned_data.get("message")

        if subject and message and subject.strip() == message.strip():
            raise ValidationError(
                _("Le sujet et le message du mail doivent etre différents")
            )
        return cleaned_data


class VideoAdminForm(forms.ModelForm):
    CATEGORY_CHOICES = [
        ("videos Ekila Musique", _("Vidéos Ekila Musique")),
        ("videos Ekila Radio", _("Vidéos Ekila Radio")),
    ]

    category = forms.ChoiceField(choices=CATEGORY_CHOICES, label=_("Catégorie"))

    class Meta:
        model = Video
        exclude = ("slug",)
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"rows": 4}),
        }
