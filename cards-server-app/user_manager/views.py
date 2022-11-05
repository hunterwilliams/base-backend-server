from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.contrib.auth.models import update_last_login

from user_manager.serializers import LoginSerializer, ChangePasswordSerializer


class AuthViewSetV1(viewsets.GenericViewSet):
    permission_classes = (AllowAny,)

    @action(methods=["POST"], detail=False, serializer_class=LoginSerializer)
    def login(self, request):
        """
        Active user logging in.
        ---
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.verify_user()
        if not user:
            return Response(
                {"non_field_errors": [("Password is incorrect.")]},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        token, _ = Token.objects.get_or_create(user=user)
        data = self.get_serializer(user).data
        data.update({"token": token.key})
        update_last_login(None, user)
        return Response(data, status=status.HTTP_200_OK)

    @action(
        methods=["POST"],
        detail=False,
        serializer_class=ChangePasswordSerializer,
        url_path="password",
        permission_classes=(IsAuthenticated,),
    )
    def change_password(self, request):
        """
        Authorized user can change password.
        ---
        """
        user = request.user
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not user.check_password(serializer.data.get("old_password")):
                return Response(
                    {"non_field_errors": ["Your old password is incorrect."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
