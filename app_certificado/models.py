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
    horas = models.IntegerField(default=0)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.nome


class Template(models.Model):
    instituicao = models.CharField(max_length=65)
    imagem = models.ImageField(upload_to='TemplatesCertificado/covers')

    def __str__(self):
        return self.instituicao


class Certificado(models.Model):
    nome = models.CharField(max_length=65)
    instituicao = models.CharField(max_length=65)
    duracao = models.IntegerField(default=0)
    categoria = models.CharField(max_length=1000)
    status = models.BooleanField(default=False)
    imagem = models.ImageField(upload_to='certificados/covers')
    aluno = models.ForeignKey(
        Aluno, on_delete=models.SET_NULL, null=True)
    template = models.ForeignKey(
        Template, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nome
    
    def update_aluno_horas(self):
        if self.status == 1 and self.aluno:
            self.aluno.horas += int(self.duracao)
            self.aluno.save()

