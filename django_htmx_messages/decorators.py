from collections.abc import Callable

from django.contrib.messages import get_messages
from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string

_hx_redirect_headers = frozenset(
    {
        "HX-Location",
        "HX-Redirect",
        "HX-Refresh",
    }
)


def inject_messages(view: Callable) -> Callable:
    """Injects messages into HTMX response."""

    def _wrapper(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        response = view(request, *args, **kwargs)

        if not request.htmx:
            return response

        if set(response.headers) & _hx_redirect_headers:
            return response

        if get_messages(request):
            response.write(
                render_to_string(
                    template_name="_messages.html",
                    context={"hx_oob": True},
                    request=request,
                )
            )

        return response

    return _wrapper
