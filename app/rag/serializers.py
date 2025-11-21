from rest_framework import serializers
from .models import Assistant, Chat


class AssistantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assistant
        fields = ('id', 'name', 'description', 'photo')


class ChatListSerializer(serializers.ModelSerializer):
    assistant = AssistantSerializer(read_only=True)

    class Meta:
        model = Chat
        fields = ('id', 'name', 'assistant', 'created_at', 'updated_at')


class ChatCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = ('id', 'name', 'assistant', 'created_at', 'updated_at')