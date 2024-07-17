from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

class JWTAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = request.COOKIES.get('access_token')
        
        print("token:" + token)
        if token:
            request.META['HTTP_AUTHORIZATION'] = f'JWT {token}'