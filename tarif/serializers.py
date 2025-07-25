from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers

from tarif.models import AdPlacement
from tarif.models import AdvertisingOffer
from tarif.models import OfferCategory
from tarif.models import OfferOption
from tarif.models import Order
from tarif.models import Payment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "password2",
            "first_name",
            "last_name",
        ]

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas")
        return data

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        user = authenticate(username=data["username"], password=data["password"])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Identifiants incorrects")


class OfferCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferCategory
        fields = "__all__"


class OfferOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferOption
        fields = "__all__"


class AdPlacementSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdPlacement
        fields = "__all__"


class AdvertisingOfferSerializer(serializers.ModelSerializer):
    category = OfferCategorySerializer(read_only=True)
    options = OfferOptionSerializer(many=True, read_only=True)
    placements = AdPlacementSerializer(many=True, read_only=True)

    support_type_display = serializers.CharField(
        source="get_support_type_display", read_only=True
    )

    class Meta:
        model = AdvertisingOffer
        fields = "__all__"
        extra_fields = ["support_type_display"]


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ("created_at", "reference", "user")
        extra_fields = ["status_display"]


class PaymentSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at", "response_data")
