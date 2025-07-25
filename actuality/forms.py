from django import forms
from django.utils.translation import gettext_lazy as _
from ckeditor.widgets import CKEditorWidget

from actuality.models import Actuality


class ActualityAdminForm(forms.ModelForm):
    CATEGORY = [
        ("Afrique", "Afrique"),
        ("Amerique", "Amerique"),
        ("Asie", "Asie"),
        ("Europe", "Europe"),
        ("Oceanie", "Oceanie"),
        ("Antarctique", "Antarctique"),
        
    ]

    TYPECHOISE = [

        ("Politique", "Politique"),
        ("Economie", "Economie"),
        ("International", "International"),
        ("Societe", "Societe"),
        ("Sante", "Sante"),
        ("Technologie", "Technologie"),
        ("Environnement", "Environnement"),
        ("Culture", "Culture"),
        ("Sports", "Sports"),
        ("Sciences", "Sciences"),
        ("Education", "Education"),
        ("Justice", "Justice"),
        ("Evenement", "Evenement"),
        ("Innovation", "Innovation"),
        ("Podcast", "Podcast"),
    ]

    category = forms.ChoiceField(
        choices=CATEGORY,
        label="Catégorie",
        widget=forms.Select(attrs={"class": "form-control", "style": "width: 300px;"}),
    )
    text = forms.CharField(
        label=_("Description de l'actualité"),
        widget=CKEditorWidget(),  
        required=False,
    )
    type = forms.ChoiceField(
        choices = TYPECHOISE,
        label = "type",
        widget=forms.Select(attrs={"class": "form-control", "style": "width: 300px"}),
    )

    
    class Meta:
        model = Actuality
        fields = ("category", "title", "source", "intitule", "image", "text", "is_up_to_date", "type", "video_link")

    def clean_title(self) -> str:
        title = self.cleaned_data.get("title", None)
        if title and len(title) < 5:
            raise forms.ValidationError(
                _("Le titre doit comporter au moins 5 caractères."),
                code="less_character",
            )
        return title
