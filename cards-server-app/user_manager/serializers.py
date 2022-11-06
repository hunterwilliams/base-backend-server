from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth import password_validation
from user_manager.models import User, Profile


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


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        password_validation.validate_password(data.get("new_password"), self.instance)

        if not data.get("new_password") or not data.get("confirm_password"):
            raise serializers.ValidationError(
                "Please enter new password and confirm it."
            )

        if data.get("new_password") != data.get("confirm_password"):
            raise serializers.ValidationError(
                "New password and confirm password do not match."
            )
        return data

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email")

    class Meta:
        model = Profile
        exclude = ("user",)

    def update_email_for_user(self, user, email):
        if user.email.casefold() != email.casefold():
            if User.objects.filter(email__iexact=email).exists():
                raise serializers.ValidationError(
                    {
                        "non_field_errors": [
                            "This email is already being used for another account."
                        ]
                    }
                )
            user.email = email
            user.save()

    def create(self, validated_data):
        user_data = validated_data.pop("user")

        new_profile = validated_data
        new_profile["user"] = self.context["user"]
        self.update_email_for_user(self.context["user"], user_data["email"])
        instance = super().create(validated_data)
        return instance

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user")
        user = instance.user
        self.update_email_for_user(user, user_data["email"])

        instance = super().update(instance, validated_data)
        return instance
