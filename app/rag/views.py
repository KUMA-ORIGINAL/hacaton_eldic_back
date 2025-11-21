from rest_framework import viewsets, mixins

from .models import Assistant, Chat
from .serializers import AssistantSerializer, ChatListSerializer, ChatCreateSerializer


class AssistantViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
):
    queryset = Assistant.objects.all().order_by("-created_at")
    serializer_class = AssistantSerializer


class ChatViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin):
    queryset = Chat.objects.all().order_by("-created_at").select_related('assistant')

    def get_serializer_class(self):
        if self.action in 'list':
            return ChatListSerializer
        return ChatCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user_id=1)
