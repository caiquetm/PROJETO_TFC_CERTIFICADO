
from django.shortcuts import redirect, render, get_list_or_404, get_object_or_404
from app_certificado.models import Certificado
from .models import Aluno, Template, Certificado
from .forms import AlunoForm, TemplateForm, CertificadoForm,CertificadoFormCriar
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
import pytesseract
from PIL import Image

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
#-----------------------------------------------------------------------------------------------------------------------------------


#CRUD Certificado-------------------------------------------------------------------------------------------------------------------
import re
def enviar_certificado(request):
    if request.method == 'POST':
        form = CertificadoForm(request.POST, request.FILES)
        if form.is_valid():
            certificado = form.save(commit=False)
            # Verifica se a imagem foi carregada corretamente
            imagem = certificado.imagem
            if imagem:
                # Carrega a imagem usando PIL
                image = Image.open(imagem)
                # Usa o pytesseract para extrair o texto da imagem
                texto_extraido = pytesseract.image_to_string(image)
                

                #PROCURAR INSTITUIÇAO NA IMAGEM----------------------------------------------
                match = re.search(r'Certificado(.*?)Certificamos', texto_extraido, re.DOTALL)
                if match:
                    instituicao_certificado = match.group(1).strip()
                    certificado.instituicao = instituicao_certificado.upper()
                else:
                    match = re.search(r'(.*?)Certificamos', texto_extraido, re.DOTALL)
                    if match:
                        instituicao_certificado = match.group(1).strip()
                        certificado.instituicao = instituicao_certificado.upper()
                #------------------------------------------------------------------------------

                #PROCURAR NOME DO ALUNO NA IMAGEM----------------------------------------------
                match = re.search(r'Certificamos que(.*?)participou', texto_extraido, re.DOTALL)
                if match:
                    nome_certificado = match.group(1).strip()
                    certificado.nome = nome_certificado.upper()
                #------------------------------------------------------------------------------

                #PROCURAR HORAS NA IMAGEM----------------------------------------------
                match = re.search(r'total de (.*?)horas', texto_extraido, re.DOTALL)
                if match:
                    horas_certificado = match.group(1).strip()
                    certificado.duracao = horas_certificado.upper()
                #------------------------------------------------------------------------------

                #PROCURAR CATEGORIA NA IMAGEM----------------------------------------------
                match = re.search(r'participou (.*?),', texto_extraido, re.DOTALL)
                if match:
                    categoria_certificado = match.group(1).strip()
                    certificado.categoria = categoria_certificado.upper()
                #------------------------------------------------------------------------------


                #linhas = texto_extraido.split('\n')
                # Processar o texto extraído e inserir nos campos do Certificado
                #certificado.nome = linhas[6].upper()
                #certificado.instituicao = linhas[2]
                #certificado.categoria = linhas[7]
                # certificado.duracao = ...  
                # Buscar o aluno no banco de dados
                try:
                    aluno = Aluno.objects.get(nome=certificado.nome)
                    certificado.aluno = aluno
                except Aluno.DoesNotExist:
                    #if is_admin:  # Verifique se o usuário é um administrador
                        return redirect('app_certificado:novo_aluno')
                    #else:
                        # message = "Aluno não encontrado. Entre em contato com o administrador."
                            # Renderizar um template com a mensagem
                        # return render(request, 'seu_template_de_mensagem.html', {'message': message})      
                #certificado.categoria = texto_extraido
                certificado.save()
                return redirect('app_certificado:sucesso')  # Redireciona para a página de sucesso
    else:
        form = CertificadoForm()
    return render(request, 'app_certificado/pages/certificado/enviar_certificado.html', {'form': form})

def sucesso(request):
    return render(request, 'app_certificado/pages/certificado/sucesso.html')

def lista_certificados(request):
    certificados = Certificado.objects.all()
    return render(request, 'app_certificado/pages/certificado/lista_certificados.html', {'certificados': certificados})

def criar_certificado(request):
    if request.method == 'POST':
        form = CertificadoFormCriar(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('app_certificado:lista_certificados')
    else:
        form = CertificadoFormCriar()
    return render(request, 'app_certificado/pages/certificado/criar_certificado.html', {'form': form})

def ver_certificado(request, certificado_id):
    certificado = get_object_or_404(Certificado, id=certificado_id)
    return render(request, 'app_certificado/pages/certificado/ver_certificado.html', {'certificado': certificado})

def search_certificados(request):
    if request.method == 'GET':
        query = request.GET.get('search', '')  # Obtém o termo de pesquisa do formulário
        certificados = Certificado.objects.filter(aluno__nome__icontains=query)
        
        return render(request, 'search.html', {'certificados': certificados, 'search_query': query})

    return render(request, 'lista_certificados.html')

def atualizar_certificado(request, certificado_id):
    certificado = get_object_or_404(Certificado, id=certificado_id)
    if request.method == 'POST':
        form = CertificadoFormCriar(request.POST, request.FILES, instance=certificado)
        if form.is_valid():
            form.save()
            return redirect('app_certificado:lista_certificados')
    else:
        form = CertificadoFormCriar(instance=certificado)
    return render(request, 'app_certificado/pages/certificado/atualizar_certificado.html', {'form': form})

def excluir_certificado(request, certificado_id):
    certificado = get_object_or_404(Certificado, id=certificado_id)
    if request.method == 'POST':
        certificado.delete()
        return redirect('app_certificado:lista_certificados')
    return render(request, 'app_certificado/pages/certificado/excluir_certificado.html', {'certificado': certificado})
#-----------------------------------------------------------------------------------------------------------------------------------