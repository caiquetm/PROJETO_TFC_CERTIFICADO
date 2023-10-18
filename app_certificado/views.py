from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'app_certificado/pages/home.html', context={'name': 'Caique'})

def aluno(request):
    return render(request, 'app_certificado/aluno.html')

def usuario(request):
    return render(request, 'app_certificado/usuario.html')

def certificado(request, id):
    return render(request, 'app_certificado/pages/certificado.html', context={'name': 'Caique'})

def template(request):
    return render(request, 'app_certificado/template.html')