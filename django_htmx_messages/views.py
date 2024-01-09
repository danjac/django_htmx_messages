from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from django_htmx_messages.decorators import inject_messages


def index(request: HttpRequest) -> HttpResponse:
    """Front page"""
    return render(request, "index.html")


@inject_messages
def send_message(request: HttpRequest) -> HttpResponse:
    """Just sends an OK message back to the user."""
    messages.success(request, "All OK!")
    return render(request, "_send_button.html", {"message_sent": True})
