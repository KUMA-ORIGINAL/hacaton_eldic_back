from django.conf import settings
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from account.serializers import UserRegisterSerializer, VerifyEmailSerializer
from account.models import User, EmailVerification

def send_verification_email(email, code):
    send_mail(
        subject="Код подтверждения вашей почты",
        message=f"Ваш код подтверждения: {code}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )


class RegisterView(APIView):
    serializer_class = UserRegisterSerializer

    """Регистрация — отправка кода на почту"""
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        code_obj = user.email_verifications.last()
        send_verification_email(user.email, code_obj.code)
        return Response({"message": "Код подтверждения отправлен на почту."}, status=status.HTTP_201_CREATED)


class VerifyEmailView(APIView):
    """Подтверждение кода и выдача JWT"""
    serializer_class = VerifyEmailSerializer

    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        code_obj = serializer.validated_data["code_obj"]

        # Подтверждаем код
        code_obj.verify()

        # Генерируем JWT
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }, status=status.HTTP_200_OK)
