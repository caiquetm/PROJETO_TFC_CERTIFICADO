from django import forms
from .models import Aluno, Template, Certificado
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
#from utils.django_forms import add_placeholder, strong_password

def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name,'')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()

def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['nome']

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
        fields = ['nome', 'instituicao', 'duracao', 'categoria','status', 'imagem', 'aluno', 'template']

class UserFormCriar(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    
    username = forms.CharField(
        label='Nome de Usuário',
        max_length=150,
        help_text=(
            'Username must have letters, numbers or one of those @.+-_. '
            'The length should be between 4 and 150 characters.'
        ),
        error_messages={
            'required': 'This field must not be empty',
            'min_length': 'Username must have at least 4 characters',
            'max_length': 'Username must have less than 150 characters',
        },
        widget=forms.TextInput(attrs={'placeholder': 'Nome de Usuário'})
    )
    email = forms.EmailField(
        label='Endereço de Email',
        max_length=254,
        help_text='The e-mail must be valid',
        widget=forms.EmailInput(attrs={'placeholder': 'Endereço de Email'})
    )
    password1 = forms.CharField(
        label='Senha',
        strip=False,
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Senha'})
    )
    password2 = forms.CharField(
        label='Confirmação de Senha',
        strip=False,
        help_text='',
        error_messages={
            'required': 'Please, repeat your password'
        },
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmação de Senha'})
    )
    is_staff = forms.BooleanField(
        label='É administrador?',
        required=False,
    )
    
    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'User e-mail ja em uso', code='invalid',
            )
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username', '')
        exists = User.objects.filter(username=username).exists()

        if exists:
            raise ValidationError(
                'Username ja em uso', code='invalid',
            )
        return username
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')  # Acesse 'password1' corretamente
        password2 = cleaned_data.get('password2')  # Acesse 'password2' corretamente

        if password1 != password2:
            #raise forms.ValidationError('Senhas devem ser iguais')
            self.add_error('password1', 'Senhas devem ser iguais')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_staff']

class UserFormEditar(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    email = forms.EmailField(
        label='Endereço de Email',
        max_length=254,
        help_text='Informe um endereço de email válido.',
        widget=forms.EmailInput(attrs={'placeholder': 'Endereço de Email'})
    )

    username = forms.CharField(
        label='Nome de Usuário',
        max_length=150,
        help_text='Escolha um nome de usuário exclusivo.',
        widget=forms.TextInput(attrs={'placeholder': 'Nome de Usuário'})
    )

    is_staff = forms.BooleanField(
        label='É administrador?',
        required=False,
    )

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        user = User.objects.filter(email=email).exclude(pk=self.instance.pk).first()

        if user:
            raise ValidationError('Endereço de email já em uso', code='invalid')

        return email

    def clean_username(self):
        username = self.cleaned_data.get('username', '')
        user = User.objects.filter(username=username).exclude(pk=self.instance.pk).first()

        if user:
            raise ValidationError('Nome de usuário já em uso', code='invalid')

        return username

    class Meta:
        model = User
        fields = ['username', 'email', 'is_staff']

class UserFormDeletar():
    ...

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        widget = forms.PasswordInput()
    )