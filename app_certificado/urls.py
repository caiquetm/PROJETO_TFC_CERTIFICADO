from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib import admin

from . import views

app_name = 'app_certificado'

urlpatterns = [
    path('', views.home, name="home"),

    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/register/', views.novo_usuario, name='user_register'),
    path('users/register/create/', views.novo_usuario_criar, name='user_create'),
    path('users/edit/<int:user_id>/', views.usuario_editar, name='user_edit'),
    path('users/delete/<int:user_id>/', views.usuario_excluir, name='user_delete'),


    #path('', views.usuario, name="usuario"),
    path('certificados/<int:id>/', views.certificado, name="certificado"),
    path('certificados/aluno/<int:aluno_id>/',views.aluno, name="aluno"),
    path('certificados/template/<int:template_id>/', views.template, name="template"),
    #path('', views.alunos, name="alunos"),

    path('alunos/', views.lista_alunos, name="lista_alunos"),
    path('alunos/novo/', views.novo_aluno, name="novo_aluno"),  
    path('alunos/editar/<int:aluno_id>/', views.editar_aluno, name="editar_aluno"),  
    path('alunos/inativar/<int:aluno_id>/', views.inativar_aluno, name="inativar_aluno"),  

    path('templates/', views.lista_templates, name='lista_templates'),
    path('templates/novo/', views.novo_template, name='novo_template'),
    path('templates/editar/<int:template_id>/', views.editar_template, name='editar_template'),
    path('templates/inativar/<int:template_id>/', views.inativar_template, name='inativar_template'),

    path('enviar-certificado/', views.enviar_certificado, name='enviar_certificado'),
    path('sucesso/', views.sucesso, name='sucesso'),
    path('certificados/', views.lista_certificados, name='lista_certificados'),
    path('certificados/criar/', views.criar_certificado, name='criar_certificado'),
    path('certificados/<int:certificado_id>/', views.ver_certificado, name='ver_certificado'),
    path('certificados/<int:certificado_id>/atualizar/', views.atualizar_certificado, name='atualizar_certificado'),
    path('certificados/<int:certificado_id>/excluir/', views.excluir_certificado, name='excluir_certificado'),

    path('login/', auth_views.LoginView.as_view(template_name='app_certificado/pages/registration/login.html'), name='login'),


]

