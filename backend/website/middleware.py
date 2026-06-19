from django.conf import settings
from django.http import HttpResponse


class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if getattr(settings, "MAINTENANCE_MODE", False):
            if not request.path.startswith("/admin/"):
                return HttpResponse(
                    "<h1>Under Maintenance</h1><p>We'll be back shortly.</p>",
                    status=503,
                )
        return self.get_response(request)
