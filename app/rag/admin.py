from django.contrib import admin

from common.base_admin import BaseModelAdmin
from .models import Assistant, Chat


@admin.register(Assistant)
class AssistantAdmin(BaseModelAdmin):
    list_display = ("id", "name", "llm_model", "embed_model", "created_at", 'detail_link')
    list_filter = ("llm_model", "embed_model", "created_at")
    search_fields = ("name", "description")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Chat)
class ChatAdmin(BaseModelAdmin):
    list_display = ("id", "name", 'assistant', "created_at", 'detail_link')
    list_filter = ("assistant",)
    search_fields = ("name",)
    readonly_fields = ("created_at", "updated_at")
