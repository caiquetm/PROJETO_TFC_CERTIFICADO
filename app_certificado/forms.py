from django import forms
from .models import Aluno, Template

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['nome', 'horas']

class TemplateForm(forms.ModelForm):
    class Meta:
        model = Template
        fields = ['instituicao', 'imagem']