from django.conf import settings

class ContentSecurityPolicyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if settings.CORS_ALLOW_ALL_ORIGINS:
            response['Content-Security-Policy'] = f"frame-ancestors 'self' {' '.join(settings.CORS_ALLOWED_ORIGINS)}"
        return response