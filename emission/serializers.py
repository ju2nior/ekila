from rest_framework import serializers
from .models import Episode
from emission.models import Emission
from emission.models import FridayEditorial
from emission.models import Poadcast
from emission.models import SubEmission
from emission.models import Categorie


class EmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emission
        fields = "__all__"


class SubEmissionSerializer(serializers.ModelSerializer):
    emission = EmissionSerializer

    class Meta:
        model = SubEmission
        fields = "__all__"


class FridayEditorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = FridayEditorial
        fields = "__all__"


class PoadcastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poadcast
        fields = "__all__"



class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = ['id', 'nom']


class EpisodeSerializer(serializers.ModelSerializer):
    categorie = serializers.CharField(source='podcast.categorie', read_only=True)
    intitule = serializers.CharField(source='podcast.intitule', read_only=True)

    class Meta:
        model = Episode
        fields = ['id', 'title', 'auteur', 'audio_url', 'fichier', 'created_at', 'categorie', 'intitule']