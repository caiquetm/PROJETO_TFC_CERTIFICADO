import tempfile
import pytest
from unittest import TestCase
from tempfile import NamedTemporaryFile
from parameterized import parameterized
from django.test import RequestFactory
from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from app_certificado.forms import UserFormCriar, AlunoForm, CertificadoForm, CertificadoFormCriar, TemplateForm
from app_certificado.models import Aluno, Template, Certificado
from app_certificado.views import home, alunos, certificados, templates, usuarios, aluno, certificado, template
from django.contrib.auth import get_user_model
User = get_user_model()

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
        form = TemplateForm(data={'instituicao': 'UNIRV', 'imagem': 'TemplatesCertificado/covers/Capturar1.PNG'})
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
        aluno = Aluno.objects.create(nome="CAIQUE TELES DE MOURA", horas=0)
        template = Template.objects.create(instituicao="Instituição XYZ", imagem="caminho/para/imagem_template.jpg")

        # Crie um arquivo temporário de imagem
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as img_file:
            img_file.write(b'fake_image_content')
            img_file.flush()
            img_data = open(img_file.name, 'rb').read()

        # Crie um arquivo de imagem carregado
        uploaded_image = SimpleUploadedFile("fake_image.jpg", img_data)

        form_data = {
            'nome': 'Certificado A',
            'instituicao': 'Instituição B',
            'duracao': '2',
            'categoria': 'Categoria X',
            'imagem': uploaded_image,
            'aluno': 1,
            'template': 3,
        }

        form = CertificadoFormCriar(data=form_data, files=form_data)
        if not form.is_valid():
            print(form.errors)  # Imprime as mensagens de erro
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



    def setUp(self):
            # Crie um usuário com o nome de usuário 'caique' para simular um conflito de nome de usuário
            User.objects.create_user(username='caique', email='caique@example.com', password='password123')

    def test_username_already_exists(self):
        # You should set up a user with an existing username before this test
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
        # You should set up a user with an existing email before this test
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

@pytest.mark.django_db
def test_alunos_view():
    request = RequestFactory().get('/alunos/')
    response = alunos(request)
    assert response.status_code == 200

@pytest.mark.django_db
def test_certificados_view():
    request = RequestFactory().get('/certificados/')
    response = certificados(request)
    assert response.status_code == 200

@pytest.mark.django_db
def test_templates_view():
    request = RequestFactory().get('/templates/')
    response = templates(request)
    assert response.status_code == 200

@pytest.mark.django_db
def test_usuarios_view():
    request = RequestFactory().get('/usuarios/')
    response = usuarios(request)
    assert response.status_code == 200

@pytest.mark.django_db
def test_aluno_view():
    aluno = Aluno.objects.create(nome="CAIQUE TELES DE MOURA", horas=0)
    request = RequestFactory().get(reverse('CAIQUE TELES DE MOURA', args=[aluno.id]))
    response = aluno(request, aluno.id)
    assert response.status_code == 200

@pytest.mark.django_db
def test_certificado_view():
    certificado = Certificado.objects.create(nome="Certificado Teste", instituicao="Instituição Teste", duracao="10", categoria="Categoria Teste")
    request = RequestFactory().get(reverse('certificado', args=[certificado.id]))
    response = certificado(request, certificado.id)
    assert response.status_code == 200

@pytest.mark.django_db
def test_template_view():
    template = Template.objects.create(instituicao="Instituição Template", imagem="templatesCertificado/covers/imagem_template.jpg")
    request = RequestFactory().get(reverse('template', args=[template.id]))
    response = template(request, template.id)
    assert response.status_code == 200

def test_search_url_is_correct(self):
    url = reverse('app_certificado:search')
    self.assertEqual(url, '/search/')

def test_search_uses_correct_view_function(self):