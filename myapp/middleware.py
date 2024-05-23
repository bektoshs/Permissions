# from django.utils.deprecation import MiddlewareMixin
# import logging

# class AuditLogMiddleware(MiddlewareMixin):
#     def proccess_request(self, request):
#         logging.getLogger('django').info(f'Access: {request.path} by {request.user}')

#     def proccess_response(self, request, response):
#         logging.getLogger('django').info(f'Response: {response.status_code} for {request.path}')
#         return response