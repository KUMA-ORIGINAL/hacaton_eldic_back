from django.db import models
from common.base_model import BaseModel


class Message(BaseModel):
    SENDER_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
    ]

    chat = models.ForeignKey(
        'Chat',
        on_delete=models.CASCADE,
        related_name="messages"
    )
    sender = models.CharField(
        max_length=50,
        choices=SENDER_CHOICES,
        default='user'  # можно по умолчанию user
    )
    content = models.TextField()  # увеличиваем лимит для длинного текста

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sender}: {self.content[:30]}"

    class Meta:
        ordering = ('-created_at',)
