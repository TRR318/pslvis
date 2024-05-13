from .models import LogEntry, Subject


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # TODO get subject id from url
        # TODO compile payload from request

        #LogEntry.objects.create(
        #    subject=Subject.objects.get(sid=sid),
        #    data=payload
        #)
        return response