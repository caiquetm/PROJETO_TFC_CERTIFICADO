from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib import admin

from . import views

app_name = 'app_certificado'

urlpatterns = [
    path('', views.home, name="home"),

    path('search/', views.search, name="search"),
    path('search/alunos/', views.search_alunos, name="search_alunos"),
    path('search/certificados/', views.search_certificados, name="search_certificados"),
    path('search/usuarios/', views.search_usuarios, name="search_usuarios"),
    path('search/templates/', views.search_templates, name="search_templates"),

    path('users/list/', views.user_list, name="user_list"),
    path('users/register/', views.novo_usuario, name="user_register"),
    path('users/register/create/', views.novo_usuario_criar, name="user_create"),
    path('users/edit/<int:user_id>/', views.usuario_editar, name="user_edit"),
    path('users/delete/<int:user_id>/', views.usuario_excluir, name="user_delete"),
    path('users/inactivate/<int:user_id>/', views.inactivate_user, name='user_inactivate'),
    path('users/activate/<int:user_id>/', views.activate_user, name='user_activate'),

    #path('salvar_certificado/', views.salvar_certificado, name='salvar_certificado'),
    path('selecionar-aluno/', views.selecionar_aluno, name='selecionar_aluno'),
    path('salvar-certificado/', views.salvar_certificado, name='salvar_certificado'),
    path('error-page/', views.error_page, name='error_page'),
    #path('', views.usuario, name="usuario"),
    path('certificados/<int:id>/', views.certificado, name="certificado"),
    path('certificados/aluno/<int:aluno_id>/',views.aluno, name="aluno"),
    #path('certificados/processar-selecao-aluno/', views.processar_selecao_aluno, name='processar_selecao_aluno'),
    #path('certificados/template/<int:template_id>/', views.template, name="template"),
    #path('', views.alunos, name="alunos"),

    path('alunos/', views.lista_alunos, name="lista_alunos"),
    path('alunos/novo/', views.novo_aluno, name="novo_aluno"),  
    path('alunos/editar/<int:aluno_id>/', views.editar_aluno, name="editar_aluno"),  
    path('alunos/inativar/<int:aluno_id>/', views.inativar_aluno, name="inativar_aluno"), 
    path('alunos/ativar/<int:aluno_id>/', views.ativar_aluno, name="ativar_aluno"), 

    path('templates/', views.lista_templates, name="lista_templates"),
    path('templates/novo/', views.novo_template, name="novo_template"),
    path('templates/editar/<int:template_id>/', views.editar_template, name="editar_template"),
    path('templates/inativar/<int:template_id>/', views.inativar_template, name="inativar_template"),
    
    path('enviar-certificado/', views.enviar_certificado, name="enviar_certificado"),
    path('sucesso/', views.sucesso, name="sucesso"),
    path('certificados/', views.lista_certificados, name="lista_certificados"),
    path('certificados/criar/', views.criar_certificado, name="criar_certificado"),
    #path('certificados/criar_autom/<int:aluno_id>/', views.criar_certificado_autom, name="criar_certificado_autom"),
    path('certificados/<int:certificado_id>/', views.ver_certificado, name="ver_certificado"),
    path('certificados/<int:certificado_id>/atualizar/', views.atualizar_certificado, name="atualizar_certificado"),
    path('certificados/<int:certificado_id>/excluir/', views.excluir_certificado, name="excluir_certificado"),
    
    path('login/', views.user_login, name="login"),
    path('login/create/', views.login_create, name="login_create"),
    path('logout/', views.user_logout, name="user_logout"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('dashboard/certificado/<int:certificado_id>/edit', views.dashboard_certificado_edit, name="dashboard_certificado_edit"),
    path('dashboard/certificado/<int:certificado_id>/activate', views.activate_certificado, name='activate_certificado'),
]

