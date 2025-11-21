from rest_framework.routers import DefaultRouter
from .views import AssistantViewSet

router = DefaultRouter()
router.register(r"assistants", AssistantViewSet, basename="assistant")

urlpatterns = router.urls
