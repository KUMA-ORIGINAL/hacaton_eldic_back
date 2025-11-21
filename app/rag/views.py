from rest_framework import viewsets
from .models import Assistant
from .serializers import AssistantSerializer


class AssistantViewSet(viewsets.ModelViewSet):
    queryset = Assistant.objects.all().order_by("-created_at")
    serializer_class = AssistantSerializer

