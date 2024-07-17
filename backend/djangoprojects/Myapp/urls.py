from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("api/auth/", include("auth.urls")),
    path("api/auth/", include("djoser.urls")),
    # アカウント
    path("api/", include("user.urls")),
    # 管理画面
    path("admin/", admin.site.urls),
]