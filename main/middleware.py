from django.http import HttpResponseForbidden

class VerificationCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated and not request.user.is_verified:
            if request.path == '/sos/':
                return HttpResponseForbidden("Account not verified")
        return None