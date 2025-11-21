import json
import logging
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

from rag.services import get_assistant_response

logger = logging.getLogger(__name__)


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        from rag.models import Chat, Message

        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f"chat_{self.chat_id}"

        # загружаем чат
        self.chat = await database_sync_to_async(Chat.objects.filter(id=self.chat_id).first)()
        if not self.chat:
            await self.close(code=4001)
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()
        await self.send_json({
            "message": "Connected",
            "user_id": self.chat.user_id,
            "assistant_id": self.chat.assistant_id,
        })

        logger.info(f"Client {self.chat.user_id} connected to chat {self.chat_id}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        logger.info(f"Chat {self.chat_id} disconnected with code {close_code}")

    async def receive(self, text_data=None):
        from rag.models import Message
        try:
            data = json.loads(text_data)
            user_text = data.get("text")
            files = data.get("files", [])
            images = data.get("images", [])

            # сохраняем user message
            await database_sync_to_async(Message.objects.create)(
                chat_id=self.chat.id, sender="user", content=user_text
            )

            # отправляем событие ассистенту
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",   # ВАЖНО!!!
                    "text": user_text,
                    "files": files,
                    "images": images,
                }
            )

        except Exception:
            logger.exception("Ошибка при получении сообщения от клиента")
            await self.send_json({"error": "Ошибка при отправке сообщения"})

    async def chat_message(self, event):
        from rag.models import Message
        """
        Сюда попадаем когда нужно отправить запрос ассистенту
        """
        user_text = event["text"]
        files = event.get("files", [])
        images = event.get("images", [])

        assistant = await database_sync_to_async(lambda: self.chat.assistant)()

        full_response = ""

        try:
            # потоковый ответ
            async for delta in get_assistant_response(
                user_text,
                chat=self.chat,
                # assistant=assistant,
                files=files,
                images=images,
            ):
                await self.send(text_data=delta)
                full_response += delta

            await self.send(text_data="[COMPLETE]")

            # сохраняем сообщение ассистента
            await database_sync_to_async(Message.objects.create)(
                chat_id=self.chat.id, sender="assistant", content=full_response
            )

        except Exception:
            logger.exception("Ошибка при обработке ответа ассистента")
            await self.send_json({"error": "Ошибка при получении ответа ассистента"})
