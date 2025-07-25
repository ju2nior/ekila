from rest_framework import serializers

from actuality.models import Actuality


class ActualitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Actuality
        fields = "__all__"
