from django.urls import path, include
from rest_framework.routers import DefaultRouter

from account.views.auth import RegisterView, VerifyEmailView
from account.views.mqtt import print_message
from account.views.user import ProfileView

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls.jwt')),
    path('print/', print_message),

    path("register/", RegisterView.as_view(), name="register"),
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
    path("profile/", ProfileView.as_view(), name="profile"),
]
