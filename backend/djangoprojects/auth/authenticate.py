from django.conf import settings
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework import exceptions
from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomJWTAuthentication(JWTAuthentication):
    """Custom authentication class"""

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            access_token = (
                request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE"]) or None
            )
        else:
            access_token = self.get_raw_token(header)
        if access_token is None:
            return None

        validated_token = self.get_validated_token(access_token)
        return self.get_user(validated_token), validated_token


# 内容は、アクセストークンが正しいものかを検証する関数。
# 期限切れの場合、リフレッシュトークンを使用しアクセストークンを再取得後、再度上記認証を
# 行うという流れである。

# つまり、いろいろな場面で検証を行う際にこちらを使うのだろうと推測される。
