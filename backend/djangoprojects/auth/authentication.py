from django.conf import settings
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework import exceptions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.exceptions import AuthenticationFailed


class CustomJWTAuthentication(JWTAuthentication):
    """Custom authentication class"""

    def authenticate(self, request):
        print("Request headers:", request.headers)
        print("Request Cookie:", request.COOKIES.get("access_token"))
        header = self.get_header(request)
        
        if header is None:
            print("Authenticaition header is none")
            access_token = request.COOKIES.get("access_token") or None
        else:
            access_token = self.get_raw_token(header)
            print("Authenticaition access_token is " + str(access_token))
        if access_token is None:
            return None

        try:
            # 4. トークンを検証
            validated_token = self.get_validated_token(access_token)
            print("Authentication validated_token is " + str(validated_token))
        except InvalidToken:
            # 5. トークンが無効な場合
            raise AuthenticationFailed("Invalid token")
        return self.get_user(validated_token), validated_token
