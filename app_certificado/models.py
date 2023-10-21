from django.db import models

# Create your models here.


class Usuario(models.Model):
    email = models.CharField(max_length=50)
    nome = models.CharField(max_length=50)
    senha = models.CharField(max_length=65)
    adm = models.BooleanField(default=False)

    def __str__(self):
        return self.nome


class Aluno(models.Model):
    nome = models.CharField(max_length=50)
    horas = models.IntegerField()

    def __str__(self):
        return self.nome
    

class Template(models.Model):
    instituicao = models.CharField(max_length=65)
    imagem = models.ImageField(upload_to='TemplatesCertificado/covers/%Y/%m/%d')

    def __str__(self):
        return self.instituicao


class Certificado(models.Model):
    nome = models.CharField(max_length=65)
    instituicao = models.CharField(max_length=65)
    duracao = models.CharField(max_length=65)
    categoria = models.CharField(max_length=65)
    status = models.BooleanField(default=False)
    imagem = models.ImageField(upload_to='certificados/covers/%Y/%m/%d')
    aluno = models.ForeignKey(
        Aluno, on_delete=models.SET_NULL, null=True)
    template = models.ForeignKey(
        Template, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nome
