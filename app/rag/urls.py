from rest_framework.routers import DefaultRouter
from rag import views

router = DefaultRouter()
router.register(r"assistants", views.AssistantViewSet, basename="assistant")
router.register(r"chats", views.ChatViewSet, basename="chats")

urlpatterns = router.urls
