from django.urls import path, include
from rest_framework import routers
from .views import (
    TokenObtainView,
    LogoutView,
    UserAPIView,
    csrf,
    TokenVerifyView,
)

router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("csrf/create/", csrf),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwtverify"),
    path("jwt/create/", TokenObtainView.as_view(), name="jwtcreate"),
    path("users/me/", UserAPIView.as_view(), name="Me"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
