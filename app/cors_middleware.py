# your_project/middleware.py

from django.utils.deprecation import MiddlewareMixin

class ContentSecurityPolicyMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response['Content-Security-Policy'] = "frame-ancestors 'self' http://localhost:8000 http://your-production-domain.com"
        return response
