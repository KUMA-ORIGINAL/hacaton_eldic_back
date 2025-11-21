from django.db import models

from common.base_model import BaseModel


class Assistant(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    photo = models.ImageField(blank=True, null=True)

    llm_model = models.CharField(max_length=255, default="gpt-4o-mini")

    system_prompt = models.TextField(default="Ты — AI ассистент.")

    openai_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ассистент"
        verbose_name_plural = "Ассистенты"
