import logging

from django.conf import settings
from django.shortcuts import render

logger = logging.getLogger(__name__)


class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if getattr(settings, "MAINTENANCE_MODE", False):
            if not request.path.startswith("/admin/"):
                return render(request, "website/503.html", status=503)
        return self.get_response(request)


class SecureHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not response.has_header("X-Content-Type-Options"):
            response["X-Content-Type-Options"] = "nosniff"
        if not response.has_header("X-Frame-Options"):
            response["X-Frame-Options"] = "DENY"
        if not response.has_header("Referrer-Policy"):
            response["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response


class CacheControlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not request.user.is_authenticated and request.method == "GET":
            if not response.has_header("Cache-Control"):
                response["Cache-Control"] = "public, max-age=60"
        return response


class ErrorLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code >= 500:
            logger.error(
                "%s %s -> %s (user=%s, ip=%s)",
                request.method, request.path,
                response.status_code,
                request.user, request.META.get("REMOTE_ADDR"),
            )
        return response
