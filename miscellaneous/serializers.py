from rest_framework import serializers

from miscellaneous.models import About
from miscellaneous.models import Cookie
from miscellaneous.models import GeneralCondition
from miscellaneous.models import LegalNotice
from miscellaneous.models import PersonalData
from miscellaneous.models import Publicity
from miscellaneous.models import Service
from miscellaneous.models import Slider
from miscellaneous.models import Video


class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = "__all__"


class CookieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cookie
        fields = "__all__"


class PersonalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalData
        fields = "__all__"


class LegalNoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalNotice
        fields = "__all__"


class GeneralConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralCondition
        fields = "__all__"


class PublicitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Publicity
        fields = "__all__"


class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = "__all__"


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = "__all__"


class ContactSerializer(serializers.Serializer):
    nom = serializers.CharField()
    prenom = serializers.CharField()
    email = serializers.EmailField()
    telephone = serializers.CharField(required=False, allow_blank=True)
    message = serializers.CharField()
    service_id = serializers.IntegerField()
    fichier = serializers.FileField(required=False)


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "name"]
