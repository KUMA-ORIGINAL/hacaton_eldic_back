from rest_framework import serializers
from .models import Assistant, Chat, Message


class AssistantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assistant
        fields = ('id', 'name', 'description', 'photo', 'system_prompt', 'llm_model')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ("id", "sender", "content", "created_at")


class ChatListSerializer(serializers.ModelSerializer):
    assistant = AssistantSerializer(read_only=True)
    messages = MessageSerializer(read_only=True, many=True)

    class Meta:
        model = Chat
        fields = ('id', 'name', 'assistant', 'created_at', 'updated_at', 'messages')


class ChatCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = ('id', 'name', 'assistant', 'created_at', 'updated_at')