from django import forms
from .models import Aluno, Template, Certificado
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['nome', 'horas']

class TemplateForm(forms.ModelForm):
    class Meta:
        model = Template
        fields = ['instituicao', 'imagem']

class CertificadoForm(forms.ModelForm):
    class Meta:
        model = Certificado
        fields = ['imagem']

class CertificadoFormCriar(forms.ModelForm):
    class Meta:
        model = Certificado
        fields = ['nome', 'instituicao', 'duracao', 'categoria', 'imagem', 'aluno', 'template']


class UserFormCriar(forms.ModelForm):
    username = forms.CharField(
        label='Nome de Usuário',
        max_length=150,
        help_text='',
        widget=forms.TextInput(attrs={'placeholder': 'Nome de Usuário'})
    )
    email = forms.EmailField(
        label='Endereço de Email',
        max_length=254,
        help_text='',
        widget=forms.EmailInput(attrs={'placeholder': 'Endereço de Email'})
    )
    password1 = forms.CharField(
        label='Senha',
        strip=False,
        help_text='',
        widget=forms.PasswordInput(attrs={'placeholder': 'Senha'})
    )
    password2 = forms.CharField(
        label='Confirmação de Senha',
        strip=False,
        help_text='',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmação de Senha'})
    )
    is_staff = forms.BooleanField(
        label='É administrador?',
        required=False,
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_staff']