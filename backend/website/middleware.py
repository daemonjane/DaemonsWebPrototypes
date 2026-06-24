import logging

from django.conf import settings
from django.http import HttpResponsePermanentRedirect
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
    csp = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com https://unpkg.com https://fonts.googleapis.com; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.tailwindcss.com https://unpkg.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self' data: blob: https://api.osimart.com; "
        "connect-src 'self' http://localhost:* https://api.osimart.com; "
        "frame-ancestors 'none';"
    )

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
        if not response.has_header("Content-Security-Policy"):
            response["Content-Security-Policy"] = self.csp
        if not response.has_header("X-Robots-Tag"):
            response["X-Robots-Tag"] = "index, follow" if not settings.DEBUG else "noindex, nofollow"
        if not response.has_header("Permissions-Policy"):
            response["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
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


class HttpsRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not settings.DEBUG and not request.is_secure():
            return HttpResponsePermanentRedirect(
                request.build_absolute_uri().replace("http://", "https://", 1)
            )
        return self.get_response(request)


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
