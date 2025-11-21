# import json
# import logging
# import mimetypes
# from typing import AsyncGenerator, List, Optional
#
# from openai import AsyncOpenAI
# from config import settings
# from rag.models import Chat, Assistant
# from channels.db import database_sync_to_async
#
# api_key = settings.OPENAI_API_KEY
# client = AsyncOpenAI(api_key=api_key)
#
# logger = logging.getLogger(__name__)
#
#
# async def get_assistant_response(
#     user_message: str,
#     chat: Chat,
#     assistant: Assistant,
#     files: Optional[List[dict]] = None,
#     images: Optional[List[dict]] = None
# ) -> AsyncGenerator[str, None]:
#
#     try:
#         # Создаём thread если нет
#         if not chat.thread_id:
#             thread = await client.beta.threads.create()
#             chat.thread_id = thread.id
#             await database_sync_to_async(chat.save)()
#             logger.info(f"🧵 Created new thread: {chat.thread_id}")
#
#         # Формируем вложения
#         attachments = [{"file_id": f["file_id"]} for f in (files or [])]
#
#         filenames_text = ""
#         if files:
#             filenames = ", ".join([f.get("filename", "unknown") for f in files])
#             filenames_text = f"\n\n(Файлы: {filenames})"
#
#         content = [{"type": "text", "text": user_message + filenames_text}]
#
#         if images:
#             for image in images:
#                 content.append({
#                     "type": "image_file",
#                     "image_file": {"file_id": image["file_id"], "detail": "low"}
#                 })
#
#         logger.info(f"📤 Sending message → thread={chat.thread_id}")
#         logger.info(f"Content: {content}")
#         logger.info(f"Attachments: {attachments}")
#
#         # Отправляем юзерское сообщение
#         await client.beta.threads.messages.create(
#             thread_id=chat.thread_id,
#             role="user",
#             content=content,
#             attachments=attachments or None,
#         )
#
#         # Запускаем run
#         logger.info(f"🚀 Starting run → assistant={assistant.openai_id}")
#
#         async with client.beta.threads.runs.stream(
#             thread_id=chat.thread_id,
#             assistant_id=assistant.openai_id
#         ) as stream:
#
#             async for event in stream:
#                 # Логируем абсолютно ВСЕ события
#                 logger.info(f"📡 EVENT '{event.event}' → data={event.data}")
#
#                 # Потоковые кусочки ответа
#                 if event.event == "thread.message.delta":
#                     delta = event.data.delta
#                     if delta and delta.content:
#                         text_chunk = delta.content[0].text.value
#                         logger.info(f"💬 DELTA: {text_chunk}")
#                         yield text_chunk
#
#                 elif event.event == "thread.run.failed":
#                     logger.error(f"Run failed: {event.data.last_error}")
#                     yield "Извините, ассистент временно недоступен."
#                     break
#
#                 # Конец
#                 elif event.event == "done":
#                     logger.info("🏁 STREAM DONE")
#                     break
#
#     except Exception:
#         logger.exception("❌ Ошибка при запросе к OpenAI API")
#         yield "Извините, произошла ошибка."
#
#
# async def upload_file_to_openai(file_data, filename: str = None):
#     mime_type, _ = mimetypes.guess_type(filename or getattr(file_data, "name", ""))
#
#     purpose = "vision" if mime_type and mime_type.startswith("image/") else "assistants"
#
#     logger.info(f"📁 Uploading file: {filename}, mime={mime_type}, purpose={purpose}")
#
#     file = await client.files.create(file=file_data, purpose=purpose)
#     logger.info(f"📁 File uploaded → id={file.id}")
#
#     return file

import json
import logging
import mimetypes
from typing import AsyncGenerator, List, Optional

from openai import AsyncOpenAI
from config import settings
from rag.models import Chat
from channels.db import database_sync_to_async

api_key = settings.OPENAI_API_KEY
client = AsyncOpenAI(api_key=api_key)

logger = logging.getLogger(__name__)


async def get_assistant_response(
    user_message: str,
    chat: Chat,
    files: Optional[List[dict]] = None,
    images: Optional[List[dict]] = None
) -> AsyncGenerator[str, None]:
    """
    Отправляет сообщение в чат и возвращает потоковые кусочки ответа.
    """

    try:
        # Формируем content
        content = [{"type": "text", "text": user_message}]

        if images:
            for image in images:
                content.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image['base64']}"}
                })

        # Формируем messages
        messages = [{"role": "user", "content": content if images else user_message}]

        logger.info(f"📤 Sending message to OpenAI")

        # Запускаем потоковое получение ответа
        stream = await client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            stream=True
        )

        async for chunk in stream:
            if chunk.choices[0].delta.content:
                text_chunk = chunk.choices[0].delta.content
                logger.info(f"💬 DELTA: {text_chunk}")
                yield text_chunk

    except Exception:
        logger.exception("❌ Ошибка при запросе к OpenAI API")
        yield "Извините, произошла ошибка."


async def upload_file_to_openai(file_data, filename: str = None):
    """
    Загружает файл в OpenAI для использования в чатах.
    """
    mime_type, _ = mimetypes.guess_type(filename or getattr(file_data, "name", ""))

    purpose = "vision" if mime_type and mime_type.startswith("image/") else "assistants"

    logger.info(f"📁 Uploading file: {filename}, mime={mime_type}, purpose={purpose}")

    file = await client.files.create(file=file_data, purpose=purpose)
    logger.info(f"📁 File uploaded → id={file.id}")

    return file