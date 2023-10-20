from django.shortcuts import render
from .models import Certificado

# Create your views here.
def home(request):
    certificados = Certificado.objects.all().order_by('-id')
    return render(request, 'app_certificado/pages/home.html', context={
        'certificados': certificados})

def aluno(request, aluno_id):
    certificados = Certificado.objects.filter(aluno__id = aluno_id).order_by('-id')
    return render(request, 'app_certificado/home.html',  context={
        'certificados': certificados})

def usuario(request):
    return render(request, 'app_certificado/usuario.html')

def certificado(request, id):
    return render(request, 'app_certificado/pages/certificado-view.html', context={
        'certificado': certificado})

def template(request):
    return render(request, 'app_certificado/template.html')