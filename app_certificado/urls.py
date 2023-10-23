from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'app_certificado'

urlpatterns = [
    path('', views.home, name="home"),
    path('', views.usuario, name="usuario"),
    path('certificados/<int:id>/', views.certificado, name="certificado"),
    path('certificados/aluno/<int:aluno_id>/',views.aluno, name="aluno"),
    path('certificados/template/<int:template_id>/', views.template, name="template"),
    path('', views.alunos, name="alunos"),

    path('alunos/', views.lista_alunos, name="lista_alunos"),  # Lista de todos os alunos
    path('alunos/novo/', views.novo_aluno, name="novo_aluno"),  # Criação de um novo aluno
    path('alunos/editar/<int:aluno_id>/', views.editar_aluno, name="editar_aluno"),  # Edição de um aluno existente
    path('alunos/inativar/<int:aluno_id>/', views.inativar_aluno, name="inativar_aluno"),  # Exclusão de um aluno

    path('templates/', views.lista_templates, name='lista_templates'),
    path('templates/novo/', views.novo_template, name='novo_template'),
    path('templates/editar/<int:template_id>/', views.editar_template, name='editar_template'),
    path('templates/inativar/<int:template_id>/', views.inativar_template, name='inativar_template'),

    path('enviar-certificado/', views.enviar_certificado, name='enviar_certificado'),
    path('sucesso/', views.sucesso, name='sucesso'),

]

