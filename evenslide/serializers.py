from rest_framework import serializers

from evenslide.models import Evenement


class EvenementSerializer(serializers.ModelSerializer):

      def validate_title(self, value):
        if len(value) < 4:
            raise serializers.ValidationError("Le titre est trop court.")
        return value

      class Meta:
         model = Evenement
         fields = "__all__"
