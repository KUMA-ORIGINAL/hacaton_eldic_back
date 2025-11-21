import json
import paho.mqtt.client as mqtt
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

# MQTT клиент
mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
mqtt_client.connect(settings.MQTT_BROKER)


@api_view(['POST'])
def print_message(request):
    payload = json.dumps(request.data)
    mqtt_client.publish(settings.MQTT_TOPIC, payload)
    return Response({"status": "ok"})
