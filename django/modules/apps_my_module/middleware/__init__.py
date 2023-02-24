import logging


logger = logging.getLogger(__name__)


class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        print('Prueba before response')

        response = self.get_response(request)

        print('Prueba after response')

        # Code to be executed for each request/response after
        # the view is called.
        logger.info('Prueba middleware')

        return response
