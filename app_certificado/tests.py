import tempfile
import pytest
from django import views
from unittest import TestCase
from django.test import TestCase
from tempfile import NamedTemporaryFile
from parameterized import parameterized
from django.test import RequestFactory
from django.test import TestCase as DjangoTestCase
from django.urls import resolve, reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from app_certificado.forms import UserFormCriar, AlunoForm, CertificadoForm, CertificadoFormCriar, TemplateForm
from app_certificado.models import Aluno, Template, Certificado
from app_certificado.views import home, certificados, aluno, certificado
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

image_path = 'media/TemplatesCertificado/covers/2023/10/21/Capturar1.PNG'
with open(image_path, 'rb') as file:
    image_content = file.read()
image_file = SimpleUploadedFile("file.png", image_content)

aluno_id = 1
template_id = 5

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
        form = TemplateForm(
            data={'instituicao': 'UNIRV'},
            files={'imagem': image_file}
        )
        self.assertTrue(form.is_valid(), form.errors)  

    def test_template_form_empty_data(self):
        form = TemplateForm(data={})
        self.assertFalse(form.is_valid())

    def test_certificado_form_valid_data(self):
        form = CertificadoForm(
            files={'imagem': image_file}
        )
        self.assertTrue(form.is_valid())

    def test_certificado_form_empty_data(self):
        form = CertificadoForm(data={})
        self.assertFalse(form.is_valid())

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


    def setUp(self):
            User.objects.create_user(username='caique', email='caique@example.com', password='password123')

    def test_username_already_exists(self):
        form_data = {
            'username': 'caique',
            'email': 'newuser@example.com',
            'password1': 'P@ssw0rd',
            'password2': 'P@ssw0rd',
            'is_staff': False,
        }
        form = UserFormCriar(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_email_already_exists(self):
        form_data = {
            'username': 'newuser',
            'email': 'caique@example.com',
            'password1': 'P@ssw0rd',
            'password2': 'P@ssw0rd',
            'is_staff': False,
        }
        form = UserFormCriar(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)



@pytest.mark.django_db
def test_home_view():
    request = RequestFactory().get('/')
    response = home(request)
    assert response.status_code == 200

class TemplateViewTests(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(username='caique', password='qwertyuiop123')
        self.staff_user.is_staff = True
        self.staff_user.save()

        self.normal_user = User.objects.create_user(username='123', password='123qwe123')
        self.normal_user.is_staff = False
        self.normal_user.save()

    def test_staff_user_can_access_novo_template(self):
        self.client.login(username='caique', password='qwertyuiop123')
        response = self.client.get(reverse('app_certificado:novo_template'))
        self.assertEqual(response.status_code, 200)

    def test_normal_user_cannot_access_novo_template(self):
        self.client.login(username='123', password='123qwe123')
        response = self.client.get(reverse('app_certificado:novo_template'))
        self.assertEqual(response.status_code, 302)

    def test_templates_view_staff_user(self):
        self.client.login(username='caique', password='qwertyuiop123')
        response = self.client.get(reverse('app_certificado:lista_templates'))
        self.assertEqual(response.status_code, 200)

    def test_templates_view_normal_user(self):
        self.client.login(username='123', password='123qwe123')
        response = self.client.get(reverse('app_certificado:lista_templates'))
        self.assertEqual(response.status_code, 302)
