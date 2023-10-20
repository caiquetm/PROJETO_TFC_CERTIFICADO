from django.db import models

# Create your models here.


class Usuario(models.Model):
    Email = models.CharField(max_length=50)
    Nome = models.CharField(max_length=50)
    Senha = models.CharField(max_length=65)
    Adm = models.BooleanField(default=False)

    def __str__(self):
        return self.Nome


class Aluno(models.Model):
    Nome = models.CharField(max_length=50)
    Horas = models.IntegerField()

    def __str__(self):
        return self.Nome
    

class Template(models.Model):
    Instituicao = models.CharField(max_length=65)
    Imagem = models.ImageField(upload_to='TemplatesCertificado/covers/%Y/%m/%d')

    def __str__(self):
        return self.Instituicao


class Certificado(models.Model):
    Nome = models.CharField(max_length=65)
    Instituicao = models.CharField(max_length=65)
    Duracao = models.CharField(max_length=65)
    Categoria = models.CharField(max_length=65)
    Status = models.BooleanField(default=False)
    Imagem = models.ImageField(upload_to='certificados/covers/%Y/%m/%d')
    Aluno = models.ForeignKey(
        Aluno, on_delete=models.SET_NULL, null=True)
    Templates = models.ForeignKey(
        Template, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.Nome
