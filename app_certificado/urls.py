from django.urls import path
from app_certificado.views import home

urlpatterns = [
    path('', home),
]
