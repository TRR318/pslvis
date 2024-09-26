from django.urls import resolve

from ..models import LogEntry, Subject


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Extract subject id from URL using Django's resolver
        resolver_match = resolve(request.path)
        subject_id = resolver_match.kwargs.get('subj_id')

        if subject_id is not None:
            try:
                subject = Subject.objects.get(id=subject_id)

                # Compile payload from request
                payload = {
                    'path': request.path,
                    'values': request.POST.dict()
                }

                # Save the log entry
                LogEntry.objects.create(
                    subject=subject,
                    data=payload
                )
            except Subject.DoesNotExist:
                pass

        return response
