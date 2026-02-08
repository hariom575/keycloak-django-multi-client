from django.urls import path
from .views import public_view, protected_view

urlpatterns = [
    path("public/", public_view),
    path("protected/", protected_view),
]
