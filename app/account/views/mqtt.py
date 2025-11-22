import json
import paho.mqtt.client as mqtt
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

# MQTT клиент
mqtt_client = mqtt.Client(clean_session=True,)
mqtt_client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
mqtt_client.connect(settings.MQTT_BROKER)


@api_view(['POST'])
def print_message(request):
    # Преобразуем данные в JSON строку с UTF-8
    payload = json.dumps(request.data, ensure_ascii=False)

    # Отправка через MQTT с кодировкой utf-8
    mqtt_client.publish(settings.MQTT_TOPIC, payload.encode('utf-8'))

    return Response({"status": "ok"})
