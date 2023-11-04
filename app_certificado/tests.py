from unittest import TestCase

import pytest
from app_certificado.forms import UserFormCriar, AlunoForm, CertificadoForm, CertificadoFormCriar, TemplateForm
from parameterized import parameterized

from django.test import TestCase as DjangoTestCase
from django.urls import reverse

# Create your tests here.
class UserRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username', 'Nome de Usuário'),
        ('email', 'Endereço de Email'),
        ('password1', 'Senha'),
        ('password2', 'Confirmação de Senha'),
    ])
    def test_fields_placeholder(self, field, placeholder):
        form = UserFormCriar()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder, placeholder)

    
    @parameterized.expand([
        ('username', 'Nome de Usuário'),
        ('email', 'Endereço de Email'),
        ('password1', 'Senha'),
        ('password2', 'Confirmação de Senha'),
    ])
    def test_fields_label(self, field, needed):
        form = UserFormCriar()
        current = form[field].field.label
        self.assertEqual(current, needed)

@pytest.mark.django_db
class FormTests(TestCase):
    def test_aluno_form_valid_data(self):
        form = AlunoForm(data={'nome': 'João', 'horas': 10})
        self.assertTrue(form.is_valid())

    def test_aluno_form_empty_data(self):
        form = AlunoForm(data={})
        self.assertFalse(form.is_valid())

    def test_template_form_valid_data(self):
        form = TemplateForm(data={'instituicao': 'UNIRV', 'imagem': 'TemplatesCertificado/covers/covers/2023/10/21/Capturar1.PNG'})
        self.assertTrue(form.is_valid())

    def test_template_form_empty_data(self):
        form = TemplateForm(data={})
        self.assertFalse(form.is_valid())

    def test_certificado_form_valid_data(self):
        form = CertificadoForm(data={})
        self.assertTrue(form.is_valid())

    def test_certificado_form_empty_data(self):
        form = CertificadoForm(data={})
        self.assertFalse(form.is_valid())

    def test_certificado_form_criar_valid_data(self):
        form_data = {
            'nome': 'CAIQUE TELES DE MOURA',
            'instituicao': 'UNIRV',
            'duracao': 22,
            'categoria': 'Gincana',
            'imagem': 'caminho/para/imagem.jpg',
            'aluno': 1, 
        }

        form = CertificadoFormCriar(data=form_data)
        self.assertTrue(form.is_valid())

    def test_certificado_form_criar_empty_data(self):
        form = CertificadoFormCriar(data={})
        self.assertFalse(form.is_valid())

@pytest.mark.django_db
class UserFormTest(TestCase):
    def test_valid_form_data(self):
        form_data = {
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'password1': 'P@ssw0rd',
            'password2': 'P@ssw0rd',
            'is_staff': False,
        }
        form = UserFormCriar(data=form_data)
        self.assertTrue(form.is_valid())

    def test_passwords_do_not_match(self):
        form_data = {
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'password1': 'P@ssw0rd',
            'password2': 'DifferentPassword',
            'is_staff': False,
        }
        form = UserFormCriar(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password1', form.errors)
        self.assertIn('password2', form.errors)

    def test_username_already_exists(self):
        # You should set up a user with an existing username before this test
        form_data = {
            'username': 'existing_user',
            'email': 'newuser@example.com',
            'password1': 'P@ssw0rd',
            'password2': 'P@ssw0rd',
            'is_staff': False,
        }
        form = UserFormCriar(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_email_already_exists(self):
        # You should set up a user with an existing email before this test
        form_data = {
            'username': 'newuser',
            'email': 'existing_user@example.com',
            'password1': 'P@ssw0rd',
            'password2': 'P@ssw0rd',
            'is_staff': False,
        }
        form = UserFormCriar(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
