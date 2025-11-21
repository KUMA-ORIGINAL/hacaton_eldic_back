from django.db.models.signals import post_save
from django.dispatch import receiver
from openai import OpenAI
from config import settings
from .models import Assistant

client = OpenAI(api_key=settings.OPENAI_API_KEY)


@receiver(post_save, sender=Assistant)
def sync_openai_assistant(sender, instance: Assistant, created, **kwargs):
    """
    Создание и обновление ассистента в OpenAI.
    """

    # --- 1. Создание ассистента ---
    if created and not instance.openai_id:
        assistant = client.beta.assistants.create(
            name=instance.name,
            instructions=instance.system_prompt,
            model=instance.llm_model,
        )

        # сохраняем ID ассистента (например "asst_123")
        instance.openai_id = assistant.id
        instance.save(update_fields=["openai_id"])
        return

    # --- 2. Обновление ассистента ---
    if instance.openai_id:
        client.beta.assistants.update(
            assistant_id=instance.openai_id,
            name=instance.name,
            instructions=instance.system_prompt,
            model=instance.llm_model,
        )
