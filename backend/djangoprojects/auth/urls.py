
from django.urls import path, include
from rest_framework import routers
from .views import LoginUserView,LogoutView,TokenObtainView,TokenRefresh,UserAPIView,refresh_get,csrf,TokenVerifyView

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('csrf/create/', csrf),
    path('jwt/verify/', TokenVerifyView.as_view(),name="jwtverify"),
    path('jwt/create/', TokenObtainView.as_view(), name='jwtcreate'),
    path('jwt/refresh/', refresh_get),
    path('jwt/newtoken/', TokenRefresh.as_view(), name='jwtrefresh'),
    # path('create/', CreateUserView.as_view(), name='create'), djoserで処理できる /users/mme
    path('users/me/', UserAPIView.as_view(), name='Me'),
    path('login/', LoginUserView.as_view(), name='loginuser'),
    path('logout/', LogoutView.as_view(), name='logout'),
]