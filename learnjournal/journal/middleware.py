"""Small middleware examples for Deck 03B.

`ResponseTimeMiddleware` demonstrates the request/response wrapper pattern with a
safe, observable side effect: one response header. `MaintenanceModeMiddleware`
shows short-circuiting a request before the view is called.
"""

from __future__ import annotations

from time import perf_counter

from django.conf import settings
from django.http import HttpResponse


class ResponseTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        started = perf_counter()
        response = self.get_response(request)
        elapsed_ms = (perf_counter() - started) * 1000
        response["X-Response-Time"] = f"{elapsed_ms:.2f}ms"
        return response


class MaintenanceModeMiddleware:
    """Return HTTP 503 when the optional classroom maintenance flag is enabled.

    Staff users and the admin/login paths remain available so an instructor can
    still get into the site. The setting defaults to False.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        enabled = getattr(settings, "MAINTENANCE_MODE", False)
        exempt_path = request.path.startswith(("/admin/", "/accounts/"))
        is_staff = getattr(request.user, "is_staff", False)
        if enabled and not exempt_path and not is_staff:
            return HttpResponse(
                "網站維護中，請稍後再試。",
                status=503,
                content_type="text/plain; charset=utf-8",
            )
        return self.get_response(request)
