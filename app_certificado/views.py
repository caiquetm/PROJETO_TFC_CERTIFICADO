
from django.shortcuts import redirect, render, get_list_or_404, get_object_or_404
from app_certificado.models import Certificado
from .models import Aluno
from .forms import AlunoForm

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
    #certificado = Certificado.objects.filter(
    #    pk = id,
    #    ).order_by('-id').first()

    certificado = get_object_or_404(Certificado,pk = id,)  
      
    return render(request, 'app_certificado/pages/certificado-view.html', context={
        'certificado': certificado,
        'is_detail_page': True})


def template(request, template_id):
    certificados = Certificado.objects.filter(template__id = template_id).order_by('-id')
    return render(request, 'app_certificado/template.html')



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