from django.conf import settings
from django.shortcuts import render


def handler404(request, exception=None, template_name=None):
    return render(request, "404.html", { "request_path": request.path,
        "exception": exception.__class__.__name__ } )


def handler500(request, *args, **argv):
    from sentry_sdk import last_event_id

    return render(request, "500.html", {
        "sentry_event_id": last_event_id(),
        "sentry_dsn": settings.SENTRY_DSN_API
    }, status=500)
