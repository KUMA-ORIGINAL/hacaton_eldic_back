from rest_framework import serializers
from account.models import User, EmailVerification
import random


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'full_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        code = f"{random.randint(100000, 999999)}"
        EmailVerification.objects.create(user=user, code=code)
        return user


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        email = attrs.get("email")
        code = attrs.get("code")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "Пользователь не найден."})

        code_obj = user.email_verifications.filter(is_verified=False).last()
        if not code_obj:
            raise serializers.ValidationError({"code": "Код не найден."})
        if code_obj.is_expired():
            raise serializers.ValidationError({"code": "Код истёк."})
        if code_obj.code != code:
            raise serializers.ValidationError({"code": "Неверный код."})

        # Сохраняем объекты в validated_data для использования во view
        attrs["user"] = user
        attrs["code_obj"] = code_obj
        return attrs
