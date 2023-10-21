
from django.shortcuts import redirect, render, get_list_or_404, get_object_or_404
from app_certificado.models import Certificado
from .models import Aluno, Template
from .forms import AlunoForm, TemplateForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# Create your views here.
def home(request):
    certificados = Certificado.objects.all().order_by('-id')
    return render(request, 'app_certificado/pages/home.html', context={
        'certificados': certificados})

def alunos(request):
    alunos = Certificado.objects.all().order_by('-id')
    return render(request, 'app_certificado/pages/aluno-view.html', context={
        'alunos': alunos})

def certificados(request):
    certificados = Certificado.objects.all().order_by('-id')
    return render(request, 'app_certificado/pages/certificado-view.html', context={
        'certificados': certificados})

def templates(request):
    templates = Certificado.objects.all().order_by('-id')
    return render(request, 'app_certificado/pages/template-view.html', context={
        'templates': templates})

def usuarios(request):
    usuarios = Certificado.objects.all().order_by('-id')
    return render(request, 'app_certificado/pages/usuario-view.html', context={
        'usuarios': usuarios})

def usuarios(request):
    usuarios = Certificado.objects.all().order_by('-id')
    return render(request, 'app_certificado/pages/usuario-view.html', context={
        'certificados': usuarios})

def aluno(request, aluno_id): 
    certificados = get_list_or_404(
        Certificado.objects.filter(
        aluno__id = aluno_id,
        ).order_by('-id')
    )
    return render(request, 'app_certificado/pages/aluno.html',  context={
        'certificados': certificados,
        'title': f'{certificados[0].aluno.nome}  - Aluno'})

def usuario(request):
    return render(request, 'app_certificado/usuario.html')

def certificado(request, id):
    certificado = get_object_or_404(Certificado,pk = id,)    
    return render(request, 'app_certificado/pages/certificado-view.html', context={
        'certificado': certificado,
        'is_detail_page': True})

def template(request, template_id):
    certificados = Certificado.objects.filter(template__id = template_id).order_by('-id')
    return render(request, 'app_certificado/template.html')








#CRUD ALUNOS------------------------------------------------------------------------------------
def lista_alunos(request):
    alunos = Aluno.objects.all()
    return render(request, 'app_certificado/pages/aluno/lista_alunos.html', {'alunos': alunos})

def novo_aluno(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('app_certificado:lista_alunos')
    else:
        form = AlunoForm()
    return render(request, 'app_certificado/pages/aluno/novo_aluno.html', {'form': form})

def editar_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, pk=aluno_id)
    if request.method == 'POST':
        form = AlunoForm(request.POST, instance=aluno)
        if form.is_valid():
            form.save()
            return redirect('app_certificado:lista_alunos')
    else:
        form = AlunoForm(instance=aluno)
    return render(request, 'app_certificado/pages/aluno/editar_aluno.html', {'form': form})

def excluir_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, pk=aluno_id)
    if request.method == 'POST':
        aluno.delete()
        return redirect('app_certificado:lista_alunos')
    return render(request, 'app_certificado/pages/aluno/excluir_aluno.html', {'aluno': aluno})

def inativar_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, pk=aluno_id)
    if request.method == 'POST':
        aluno.status = True
        aluno.save()
        return redirect('app_certificado:lista_alunos')
    return render(request, 'app_certificado/pages/aluno/inativar_aluno.html', {'aluno': aluno})
#-----------------------------------------------------------------------------------------------

#CRUD templates---------------------------------------------------------------------------------
def lista_templates(request):
    templates = Template.objects.all()
    return render(request, 'app_certificado/pages/templateCertificado/lista_templates.html', {'templates': templates})

def novo_template(request):
    if request.method == 'POST':
        form = TemplateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('app_certificado:lista_templates')
    else:
        form = TemplateForm()
    return render(request, 'app_certificado/pages/templateCertificado/novo_template.html', {'form': form})

def editar_template(request, template_id):
    template = get_object_or_404(Template, pk=template_id)
    if request.method == 'POST':
        form = TemplateForm(request.POST, request.FILES, instance=template)
        if form.is_valid():
            form.save()
            return redirect('app_certificado:lista_templates')
    else:
        form = TemplateForm(instance=template)
    return render(request, 'app_certificado/pages/templateCertificado/editar_template.html', {'form': form, 'template': template})

def inativar_template(request, template_id):
    template = get_object_or_404(Template, pk=template_id)
    if request.method == 'POST':
        template.delete()
        return redirect('app_certificado:lista_templates')
    return render(request, 'app_certificado/pages/templateCertificado/inativar_template.html', {'template': template})
#-----------------------------------------------------------------------------------------------------------------------------------

#CRUD User--------------------------------------------------------------------------------------------------------------------------
