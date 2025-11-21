from django.db import models

from common.base_model import BaseModel


class Assistant(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    photo = models.ImageField(blank=True, null=True)

    llm_model = models.CharField(max_length=255, default="gpt-4o-mini")
    embed_model = models.CharField(max_length=255, default="text-embedding-3-small")

    top_k = models.IntegerField(default=5)
    chunk_size = models.IntegerField(default=800)
    chunk_overlap = models.IntegerField(default=200)

    system_prompt = models.TextField(default="Ты — AI ассистент.")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ассистент"
        verbose_name_plural = "Ассистенты"