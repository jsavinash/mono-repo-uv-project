"""
accounts/views.py ─ Registration, login, logout.
"""

from django.http import HttpResponse


def hello_world_view(request):
    return HttpResponse("<h1>Hello, world!</h1>")
