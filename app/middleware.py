import re

from django.urls import resolve

from .models import LogEntry, Subject

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Extract subject id from URL using Django's resolver
        resolver_match = resolve(request.path)
        subject_id = resolver_match.kwargs.get('subject')

        if subject_id:
            try:
                subject = Subject.objects.get(id=subject_id)
            except Subject.DoesNotExist:
                subject = None

            if subject:
                # Compile payload from request
                payload = {
                    'method': request.method,
                    'path': request.path,
                    'values': request.GET.dict()
                }
                
                # Save the log entry
                LogEntry.objects.create(
                    subject=subject,
                    data=payload
                )

        return response
