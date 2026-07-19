from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user model."""

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "phone_number",
            "bio",
            "avatar",
            "date_of_birth",
            "email_verified",
            "is_online",
            "last_activity",
            "email_notifications",
            "theme",
            "date_joined",
        )
        read_only_fields = (
            "id",
            "email_verified",
            "is_online",
            "last_activity",
            "date_joined",
        )


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("username", "email", "password", "password_confirm", "phone_number")

    def validate(self, attrs):
        if attrs["password"] != attrs.pop("password_confirm"):
            raise serializers.ValidationError(
                {"password_confirm": "Passwords do not match."}
            )
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile."""

    class Meta:
        model = User
        fields = (
            "phone_number",
            "bio",
            "avatar",
            "date_of_birth",
            "email_notifications",
            "theme",
        )


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change."""

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
    new_password_confirm = serializers.CharField(required=True, min_length=8)

    def validate(self, attrs):
        if attrs["new_password"] != attrs.pop("new_password_confirm"):
            raise serializers.ValidationError(
                {"new_password_confirm": "Passwords do not match."}
            )
        return attrs


class CustomTokenObtainPairSerializer(serializers.Serializer):
    """Custom JWT token obtain serializer."""

    email = serializers.EmailField()
    password = serializers.CharField()
