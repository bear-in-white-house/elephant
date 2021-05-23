from uuid import uuid4
import logging

from django.utils.deprecation import MiddlewareMixin

from elephant import local


logger = logging.getLogger(__name__)


class RequestIdMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request_id = uuid4().hex
        request.request_id = request_id
        local.request_id = request_id
        logger.info(f'request begin: [{request.path}] [{request.method}] [{request.GET}] [{request.POST}]')

    def process_response(self, request, response):
        logger.info(f'request end: [{request.path}] [{request.method}]')
        try:
            del local.request_id
        except AttributeError:
            pass
        return response
