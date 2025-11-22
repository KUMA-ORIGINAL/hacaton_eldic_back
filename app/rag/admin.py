from django.contrib import admin

from common.base_admin import BaseModelAdmin
from .models import Assistant, Chat, Message


@admin.register(Assistant)
class AssistantAdmin(BaseModelAdmin):
    list_display = ("id", 'user', "name", 'llm_model', "created_at", 'detail_link')
    list_filter = ("created_at", 'user', 'llm_model')
    search_fields = ("name", "description")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Chat)
class ChatAdmin(BaseModelAdmin):
    list_display = ("id", 'user', "name", 'assistant', "created_at", 'detail_link')
    list_filter = ("assistant", 'user', 'created_at')
    search_fields = ("name",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(Message)
class MessageAdmin(BaseModelAdmin):
    list_display = ("id", 'chat', "sender", "created_at", 'detail_link')
    list_filter = ("chat",)
    search_fields = ("name",)
    readonly_fields = ("created_at", "updated_at")
