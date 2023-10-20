from django.urls import path

from . import views

urlpatterns = [
    path('', views.home),
    path('', views.aluno),
    path('', views.usuario),
    path('certificados/<int:id>/', views.certificado),
    path('', views.template),
]

