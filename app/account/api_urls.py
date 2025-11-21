from django.urls import path, include
from rest_framework.routers import DefaultRouter

from account.views.mqtt import print_message

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls.jwt')),
    path('print/', print_message),
]
