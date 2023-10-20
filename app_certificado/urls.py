from django.urls import path

from . import views

app_name = 'app_certificado'

urlpatterns = [
    path('', views.home, name="home"),
    path('', views.aluno),
    path('', views.usuario),
    path('certificados/<int:id>/', views.certificado, name="certificado"),
    path('', views.template),
]

