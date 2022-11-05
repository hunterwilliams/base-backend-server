from django.contrib.auth import authenticate
from rest_framework import serializers

from user_manager.models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if email and password:
            try:
                user = User.objects.get(email__iexact=email)
                if not user.is_active:
                    raise serializers.ValidationError("This email is inactive.")
            except User.DoesNotExist:
                raise serializers.ValidationError("This email does not exist.")
        else:
            raise serializers.ValidationError("Email and password are required.")

        return data

    def verify_user(self):
        return authenticate(
            email=self.validated_data["email"], password=self.validated_data["password"]
        )

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

