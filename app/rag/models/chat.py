from django.contrib.auth import get_user_model
from django.db import models

from common.base_model import BaseModel

User = get_user_model()


class Chat(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="chats"
    )
    assistant = models.ForeignKey(
        'Assistant',
        on_delete=models.CASCADE,
        related_name="chats"
    )
    thread_id = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or f"Chat {self.id}"
