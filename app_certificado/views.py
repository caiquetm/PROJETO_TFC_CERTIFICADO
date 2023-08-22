from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'app_certificado/pages/home.html')

def aluno(request):
    return render(request, 'app_certificado/aluno.html')

def usuario(request):
    return render(request, 'app_certificado/usuario.html')

def certificado(request):
    return render(request, 'app_certificado/certificado.html')

def template(request):
    return render(request, 'app_certificado/template.html')