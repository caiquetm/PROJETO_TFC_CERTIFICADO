from django.urls import path

from . import views

app_name = 'app_certificado'

urlpatterns = [
    path('', views.home, name="home"),
    path('', views.usuario),
    path('certificados/<int:id>/', views.certificado, name="certificado"),

    path('certificados/aluno/<int:aluno_id>/',
          views.aluno, name="aluno"),

    path('certificados/template/<int:template_id>/', views.template, name="template"),

    path('', views.alunos, name="alunos"),

]

