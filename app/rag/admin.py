from django.contrib import admin

from common.base_admin import BaseModelAdmin
from .models import Assistant


@admin.register(Assistant)
class AssistantAdmin(BaseModelAdmin):
    list_display = ("id", "name", "llm_model", "embed_model", "created_at")
    list_filter = ("llm_model", "embed_model", "created_at")
    search_fields = ("name", "description")
    readonly_fields = ("created_at", "updated_at")
