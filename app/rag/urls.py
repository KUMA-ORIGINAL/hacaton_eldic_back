from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rag import views

router = DefaultRouter()
router.register(r"assistants", views.AssistantViewSet, basename="assistant")
router.register(r"chats", views.ChatViewSet, basename="chats")

urlpatterns = [
    path('', include(router.urls)),
    path('llm-models/', views.llm_models_list, name='llm-models-list'),
]
