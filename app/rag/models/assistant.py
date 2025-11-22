from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Assistant(models.Model):
    MODEL_CHOICES = [
        ("gpt-5", "gpt-5"),
        ("gpt-5-nano", "gpt-5-nano"),
        ("gpt-4.1", "gpt-4.1"),
        ("gpt-4.1-mini", "gpt-4.1-mini"),
        ("gpt-4.1-nano", "gpt-4.1-nano"),
        ("gpt-4o", "GPT-4o"),
        ("gpt-4", "GPT-4"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="assistants",
        verbose_name="Пользователь"
    )

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    photo = models.ImageField(blank=True, null=True)

    llm_model = models.CharField(
        max_length=50,
        choices=MODEL_CHOICES,
        default="gpt-5-mini"
    )

    system_prompt = models.TextField(default="Ты — AI ассистент.")

    openai_id = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего обновления")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ассистент"
        verbose_name_plural = "Ассистенты"
