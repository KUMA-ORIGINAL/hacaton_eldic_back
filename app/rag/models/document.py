from django.db import models
from common.base_model import BaseModel


class Document(BaseModel):
    title = models.CharField(max_length=255)
    content = models.TextField()
    embedding = models.BinaryField(blank=True, null=True)  # вектор хранится здесь
