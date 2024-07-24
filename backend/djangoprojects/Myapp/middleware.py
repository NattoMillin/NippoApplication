
import logging


class SameSiteMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        from Myapp import settings

        for key in response.cookies.keys():
            # response.cookies[key]['samesite'] = 'Lax' if settings.DEBUG else 'None'
            response.cookies[key]['samesite'] = 'None'
            response.cookies[key]['secure'] = not settings.DEBUG
        return response


logger = logging.getLogger(__name__)

class LogRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.log_request(request)
        response = self.get_response(request)
        return response
    # test

    def log_request(self, request):
        logger.info("Request Method: %s", request.method)
        logger.info("Request Path: %s", request.get_full_path())
        logger.info("Request Headers: %s", dict(request.headers))
        if request.body:
            logger.info("Request Body: %s", request.body.decode('utf-8'))
