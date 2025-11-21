from rest_framework import viewsets, mixins, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Assistant, Chat
from .serializers import AssistantSerializer, ChatListSerializer, ChatCreateSerializer


class AssistantViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
):
    serializer_class = AssistantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Показываем только ассистентов текущего пользователя
        return Assistant.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        # Привязываем ассистента к текущему пользователю
        serializer.save(user=self.request.user)


class ChatViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin
):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Только чаты пользователя
        return Chat.objects.filter(user=self.request.user).order_by("-created_at").select_related('assistant')

    def get_serializer_class(self):
        if self.action == 'list':
            return ChatListSerializer
        return ChatCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def llm_models_list(request):
    """
    Возвращает список доступных моделей LLM для выбора.
    """
    models = [choice[0] for choice in Assistant.MODEL_CHOICES]
    return Response(models)
