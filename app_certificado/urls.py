from django.urls import path

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

]

