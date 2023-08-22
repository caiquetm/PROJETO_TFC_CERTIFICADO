from django.urls import path
from app_certificado.views import home, aluno, usuario, certificado, template

urlpatterns = [
    path('', home),
    path('', aluno),
    path('', usuario),
    path('', certificado),
    path('', template),
]
