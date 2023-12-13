
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect, render, get_list_or_404, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Aluno, Template, Certificado
from .forms import AlunoForm, TemplateForm, CertificadoForm, CertificadoFormCriar, LoginForm, UserFormCriar, UserFormEditar
import pytesseract
from PIL import Image
from django.db.models import Q

# Create your views here.
def is_staff(user):
    return user.is_staff

def home(request):
    certificados = Certificado.objects.all().order_by('-id')
    return render(request, 'app_certificado/pages/home.html', context={
        'certificados': certificados})

def certificados(request):
    certificados = Certificado.objects.all().order_by('-id')
    return render(request, 'app_certificado/pages/certificado-view.html', context={
        'certificados': certificados})

def aluno(request, aluno_id): 
    certificados = get_list_or_404(
        Certificado.objects.filter(
        aluno__id = aluno_id,
        ).order_by('-id')
    )
    return render(request, 'app_certificado/pages/aluno.html',  context={
        'certificados': certificados,
        'title': f'{certificados[0].aluno.nome}  - Aluno'})

def certificado(request, id):
    certificado = get_object_or_404(Certificado,pk = id,)    
    return render(request, 'app_certificado/pages/certificado-view.html', context={
        'certificado': certificado,
        'is_detail_page': True})



#CRUD ALUNOS------------------------------------------------------------------------------------
@user_passes_test(is_staff, login_url='app_certificado:login', redirect_field_name='next')
def lista_alunos(request):
    alunos = Aluno.objects.all()
    return render(request, 'app_certificado/pages/aluno/lista_alunos.html', {'alunos': alunos})

@user_passes_test(is_staff, login_url='app_certificado:login', redirect_field_name='next')
def novo_aluno(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('app_certificado:lista_alunos')
    else:
        form = AlunoForm()
    return render(request, 'app_certificado/pages/aluno/novo_aluno.html', {'form': form})

@user_passes_test(is_staff, login_url='app_certificado:login', redirect_field_name='next')
def editar_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, pk=aluno_id)
    certificados = Certificado.objects.filter(aluno=aluno)

    if certificados.exists():
        lista_alunos_url = reverse('app_certificado:lista_alunos')
        return HttpResponse(f"Não é possível editar este aluno, pois existem certificados associados a ele. <a href='{lista_alunos_url}'>Voltar para a lista de alunos</a>")
    
    if request.method == 'POST':
        form = AlunoForm(request.POST, instance=aluno)
        if form.is_valid():
            form.save()
            return redirect('app_certificado:lista_alunos')
    else:
        form = AlunoForm(instance=aluno)
    return render(request, 'app_certificado/pages/aluno/editar_aluno.html', {'form': form})

@user_passes_test(is_staff, login_url='app_certificado:login', redirect_field_name='next')
def excluir_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, pk=aluno_id)
    certificados = Certificado.objects.filter(aluno=aluno)

    if certificados.exists():
        lista_alunos_url = reverse('app_certificado:lista_alunos')
        return HttpResponse(f"Não é possível excluir este aluno, pois existem certificados associados a ele. <a href='{lista_alunos_url}'>Voltar para a lista de alunos</a>")

    if request.method == 'POST':
        aluno.delete()
        return redirect('app_certificado:lista_alunos')
    return render(request, 'app_certificado/pages/aluno/excluir_aluno.html', {'aluno': aluno})

@user_passes_test(is_staff, login_url='app_certificado:login', redirect_field_name='next')
def inativar_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, pk=aluno_id)
    certificados = Certificado.objects.filter(aluno=aluno)

    if certificados.exists():
        lista_alunos_url = reverse('app_certificado:lista_alunos')
        return HttpResponse(f"Não é possível inativar este aluno, pois existem certificados associados a ele. <a href='{lista_alunos_url}'>Voltar para a lista de alunos</a>")

    if request.method == 'POST':
        aluno.status = True
        aluno.save()
        return redirect('app_certificado:lista_alunos')
    return render(request, 'app_certificado/pages/aluno/inativar_aluno.html', {'aluno': aluno})

@user_passes_test(is_staff, login_url='app_certificado:login', redirect_field_name='next')
def ativar_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, pk=aluno_id)
    if request.method == 'POST':
        aluno.status = False  # Defina o status como False para ativar o aluno
        aluno.save()
        return redirect('app_certificado:lista_alunos')
    return render(request, 'app_certificado/pages/aluno/ativar_aluno.html', {'aluno': aluno})
#-----------------------------------------------------------------------------------------------


#CRUD templates---------------------------------------------------------------------------------
@user_passes_test(is_staff, login_url='app_certificado:login', redirect_field_name='next')
def lista_templates(request):
    templates = Template.objects.all()
    return render(request, 'app_certificado/pages/templateCertificado/lista_templates.html', {'templates': templates})

@user_passes_test(is_staff, login_url='app_certificado:login', redirect_field_name='next')
def novo_template(request):
    if request.method == 'POST':
        form = TemplateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('app_certificado:lista_templates')
    else:
        form = TemplateForm()
    return render(request, 'app_certificado/pages/templateCertificado/novo_template.html', {'form': form})

@user_passes_test(is_staff, login_url='app_certificado:login', redirect_field_name='next')
def editar_template(request, template_id):
    template = get_object_or_404(Template, pk=template_id)
    certificados = Certificado.objects.filter(template=template)

    if certificados.exists():
        lista_templates_url = reverse('app_certificado:lista_templates')
        return HttpResponse(f"Não é possível editar este template, pois existem certificados associados a ele. <a href='{lista_templates_url}'>Voltar para a lista de templates</a>")

    if request.method == 'POST':
        form = TemplateForm(request.POST, request.FILES, instance=template)
        if form.is_valid():
            form.save()
            return redirect('app_certificado:lista_templates')
    else:
        form = TemplateForm(instance=template)
    return render(request, 'app_certificado/pages/templateCertificado/editar_template.html', {'form': form, 'template': template})

@user_passes_test(is_staff, login_url='app_certificado:login', redirect_field_name='next')
def inativar_template(request, template_id):
    template = get_object_or_404(Template, pk=template_id)
    certificados = Certificado.objects.filter(template=template)

    if certificados.exists():
        lista_templates_url = reverse('app_certificado:lista_templates')
        return HttpResponse(f"Não é possível inativar este template, pois existem certificados associados a ele. <a href='{lista_templates_url}'>Voltar para a lista de templates</a>")

    if request.method == 'POST':
        template.delete()
        return redirect('app_certificado:lista_templates')

    return render(request, 'app_certificado/pages/templateCertificado/inativar_template.html', {'template': template})
#-----------------------------------------------------------------------------------------------------------------------------------


#CRUD User--------------------------------------------------------------------------------------------------------------------------
@user_passes_test(is_staff, login_url='app_certificado:login', redirect_field_name='next')
def user_list(request):
    users = User.objects.all()  # Retrieve all users from the database
    return render(request, 'app_certificado/pages/user/user_list.html', {
        'users': users,
    })

@user_passes_test(is_staff, login_url='app_certificado:login', redirect_field_name='next')
def novo_usuario(request):
    register_form_data = request.session.get('register_form_data', None)
    form = UserFormCriar(register_form_data)
    return render(request, 'app_certificado/pages/user/user_form.html', {
        'form': form
    })

@user_passes_test(is_staff, login_url='app_certificado:login', redirect_field_name='next')
def novo_usuario_criar(request):
    if request.method == 'POST':
        form = UserFormCriar(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            user = User(username=username, email=email)
            user.set_password(password)
            user.save()

            messages.success(request, 'Usuário criado com sucesso')

            # Limpa os dados da sessão
            if 'register_form_data' in request.session:
                del request.session['register_form_data']

            return redirect('app_certificado:user_list')
    else:
        form = UserFormCriar()

    return render(request, 'app_certificado/pages/user/user_create.html', {'form': form})

@user_passes_test(is_staff, login_url='app_certificado:login', redirect_field_name='next')
def usuario_editar(request, user_id):
    
    user = User.objects.get(pk=user_id)

    if request.method == 'POST':
        form = UserFormEditar(request.POST, instance=user)  
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário atualizado com sucesso')
            if 'register_form_data' in request.session:
                del request.session['register_form_data']
            return redirect('app_certificado:user_list')  # Redirect to the user list after editing

    else:
        form = UserFormEditar(instance=user)

    return render(request, 'app_certificado/pages/user/user_edit.html', {
        'form': form,
        'user': user,
    })

@user_passes_test(is_staff, login_url='app_certificado:login', redirect_field_name='next')
def usuario_excluir(request, user_id):
    # Recupere o usuário com base no ID fornecido
    user = User.objects.get(pk=user_id)

    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Usuário excluído com sucesso')
        return redirect('app_certificado:user_list')  # Redirecione para a lista de usuários após a exclusão

    return render(request, 'app_certificado/pages/user/user_confirm_delete.html', {'user': user})

@user_passes_test(is_staff, login_url='app_certificado:login', redirect_field_name='next')
def inactivate_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    
    # Marque o usuário como inativo
    user.is_active = False
    user.save()
    
    return HttpResponseRedirect(reverse('app_certificado:user_list'))

@user_passes_test(is_staff, login_url='app_certificado:login', redirect_field_name='next')
def activate_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    
    # Marque o usuário como ativo
    user.is_active = True
    user.save()
    
    return HttpResponseRedirect(reverse('app_certificado:user_list'))

def user_login(request):
    form = LoginForm()
    return render(request, 'app_certificado/pages/user/login.html', {
        'form': form,
        'form_action': reverse('app_certificado:login_create')
    })

def login_create(request):
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', '')
        )
        if authenticated_user is not None:
            messages.success(request, 'Logado com sucesso')
            auth_login(request, authenticated_user)
            if authenticated_user.is_staff:
                return redirect('app_certificado:dashboard')  
            else:
                return redirect('app_certificado:home')  
        else:
            messages.error(request, 'Credenciais Inválidas')
    else:
        messages.error(request, 'Erro ao validar dados')

    return redirect('app_certificado:login') 

@login_required(login_url='app_certificado:login', redirect_field_name='next')
def user_logout(request):
    if not request.POST:
        return redirect(reverse('app_certificado:login'))
    
    logout(request)
    return redirect(reverse('app_certificado:login'))

@user_passes_test(is_staff, login_url='app_certificado:login', redirect_field_name='next')
def dashboard(request):
    certificados = Certificado.objects.filter(
        status = False,
    )
    return render(request, 'app_certificado/pages/user/dashboard.html', {
        'certificados': certificados,
    })

@user_passes_test(is_staff, login_url='app_certificado:login', redirect_field_name='next')
def dashboard_certificado_edit(request, certificado_id):
    certificado = get_object_or_404(Certificado, id=certificado_id)
    if request.method == 'POST':
        form = CertificadoFormCriar(request.POST, request.FILES, instance=certificado)
        if form.is_valid():
            form.save()
            return redirect('app_certificado:dashboard')
    else:
        form = CertificadoFormCriar(instance=certificado)
    return render(request, 'app_certificado/pages/user/dashboard_certificado.html', {'form': form})
#-----------------------------------------------------------------------------------------------------------------------------------


#CRUD Certificado-------------------------------------------------------------------------------------------------------------------
import re
@login_required(login_url='app_certificado:login', redirect_field_name='next')
def enviar_certificado(request):
    if request.method == 'POST':
        form = CertificadoForm(request.POST, request.FILES)
        if form.is_valid():
            certificado = form.save(commit=False)
            # Verifica se a imagem foi carregada corretamente
            imagem = certificado.imagem
            if imagem:
                try:
                    # Carrega a imagem usando PIL
                    image = Image.open(imagem)
                    # Usa o pytesseract para extrair o texto da imagem
                    texto_extraido = pytesseract.image_to_string(image)
                    

                    #PROCURAR INSTITUIÇAO NA IMAGEM----------------------------------------------
                    match = re.search(r'Certificado(.*?)Certificamos', texto_extraido, re.DOTALL)
                    if match:
                        instituicao_certificado = match.group(1).strip()
                        certificado.instituicao = instituicao_certificado.upper()
                    else:
                        match = re.search(r'(.*?)Certificamos', texto_extraido, re.DOTALL)
                        if match:
                            instituicao_certificado = match.group(1).strip()
                            certificado.instituicao = instituicao_certificado.upper()
                    #------------------------------------------------------------------------------

                    #PROCURAR NOME DO ALUNO NA IMAGEM----------------------------------------------
                    match = re.search(r'Certificamos que(.*?)participou', texto_extraido, re.DOTALL)
                    if match:
                        nome_certificado = match.group(1).strip()
                        certificado.nome = nome_certificado.upper()
                    #------------------------------------------------------------------------------

                    #PROCURAR HORAS NA IMAGEM----------------------------------------------
                    match = re.search(r'total de (.*?)horas', texto_extraido, re.DOTALL)
                    if match:
                        horas_certificado = match.group(1).strip()
                        certificado.duracao = horas_certificado.upper()
                    #------------------------------------------------------------------------------

                    #PROCURAR CATEGORIA NA IMAGEM----------------------------------------------
                    match = re.search(r'participou (.*?),', texto_extraido, re.DOTALL)
                    if match:
                        categoria_certificado = match.group(1).strip()
                        certificado.categoria = categoria_certificado.upper()
                    #------------------------------------------------------------------------------

                    # Additional Validation Checks
                    valid_phrases = ['Certificamos que']
                    is_valid_certificate = all(phrase in texto_extraido for phrase in valid_phrases)
                    print(f'certificado_data set in session: {valid_phrases}')
                    print(f'certificado_data set in session: {texto_extraido}')
                    print(f'certificado_data set in session: {is_valid_certificate}')

                    confidence_threshold = 80  # Adjust as needed
                    if image.info.get('dpi', (0, 0))[0] < confidence_threshold or not is_valid_certificate:
                        messages.error(request, 'A imagem não atende aos critérios de validação.')
                        return redirect('app_certificado:error_page')
                    

                    # Verifica se a palavra 'UNIRV' está no texto_extraido
                    if 'UNIRV' in certificado.instituicao:
                        try:
                            template = Template.objects.get(instituicao__iexact='UNIRV')
                            certificado.template = template
                        except Template.DoesNotExist:
                            print("Instituição 'UNIRV' não encontrada no banco de dados")   
                            return redirect('app_certificado:novo_template')

                    imagem_url = certificado.imagem.url if certificado.imagem else None
                    # Save the certificado_data in the session
                    certificado_data = {
                            'instituicao': certificado.instituicao,
                            'nome': certificado.nome,
                            'duracao': certificado.duracao,
                            'categoria': certificado.categoria,
                            'imagem': imagem_url,
                            'template': certificado.template.id if certificado.template else None,
                        }
                    request.session['certificado_data'] = certificado_data

                        # Add this print statement to check if certificado_data is set correctly
                    print(f'certificado_data set in session: {certificado_data}')





                    # Buscar o aluno no banco de dados
                    try:
                        aluno = Aluno.objects.get(nome=certificado.nome)
                        certificado.aluno = aluno
                    except Aluno.DoesNotExist:
                        print('Aluno não encontrado. Redirecionando para novo_aluno...')
                        return redirect('app_certificado:novo_aluno')
                    except Aluno.MultipleObjectsReturned:
                        # Handle the case where multiple Aluno objects have the same name
                        matching_alunos = Aluno.objects.filter(nome=certificado.nome)
                        if matching_alunos.exists():
                            # If there are matching alunos, let the user choose one
                            print('Múltiplos alunos encontrados. Redirecionando para handle_multiple_alunos...')
                            return handle_multiple_alunos(request, certificado, matching_alunos)
                        
                        # If no matching alunos, redirect to an error page or handle accordingly
                        messages.error(request, 'Erro: Múltiplos alunos encontrados com o mesmo nome.')
                        return redirect('app_certificado:error_page')  # Redirect to an error page


                    existing_certificates = Certificado.objects.filter(
                            Q(nome=certificado.nome) & Q(instituicao=certificado.instituicao) & Q(duracao=certificado.duracao)
                    )
                        
                    if existing_certificates.exists():
                            # A similar certificate already exists, handle this case (e.g., show an error message)
                            messages.error(request, 'Um certificado semelhante já existe no banco de dados.')
                    else:
                            # Save the certificate if no similar certificate exists
                            certificado.save()
                            messages.success(request, 'Certificado salvo com sucesso.')
                            return redirect('app_certificado:sucesso')  # Redirect to the success page
                except Exception as e:
                    # Handle exceptions during image processing or text extraction
                    messages.error(request, f'Erro durante o processamento da imagem: {str(e)}')
                    return redirect('app_certificado:error_page')
    else:
        form = CertificadoForm()
    return render(request, 'app_certificado/pages/certificado/enviar_certificado.html', {'form': form})


def handle_multiple_alunos(request, certificado, alunos):
    # Render a page to let the user choose from the list of matching alunos
    return render(
        request,
        'app_certificado/pages/certificado/selecionar_aluno.html',
        {'certificado': certificado, 'alunos': alunos}
    )

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Aluno, Certificado
from django.core.exceptions import ValidationError

from django.shortcuts import render

from django.shortcuts import redirect, render

def selecionar_aluno(request):
    certificado_data = request.session.get('certificado_data', {})

    if not certificado_data:
        messages.error(request, 'Certificado data not found in the session.')
        return redirect('app_certificado:error_page')

    if request.method == 'POST':
        certificado_id = request.POST.get('certificado_id')
        aluno_id = request.POST.get('aluno_id')

        # Check if the provided aluno_id is valid
        try:
            aluno_id = int(aluno_id)
            aluno = Aluno.objects.get(pk=aluno_id)
        except (ValueError, Aluno.DoesNotExist):
            messages.error(request, 'Aluno not found with the provided ID.')
            return redirect('app_certificado:error_page')  # Redirect to an error page

        # Check if the provided certificado_id is valid
        try:
            certificado_id = int(certificado_id)
            certificado = Certificado.objects.get(pk=certificado_id)
        except (ValueError, Certificado.DoesNotExist):
            messages.error(request, 'Certificado not found with the provided ID.')
            return redirect('app_certificado:error_page')  # Redirect to an error page

        # Associate the aluno with the certificado
        certificado.aluno = aluno

        try:
            # Save the certificado with the associated aluno
            certificado.save()
            messages.success(request, 'Aluno associado ao certificado com sucesso.')
            return redirect('app_certificado:sucesso')  # Redirect to the success page
        except Exception as e:
            # Handle any unexpected errors during the save process
            messages.error(request, f'Error associating aluno to certificado: {e}')
            return redirect('app_certificado:error_page')  # Redirect to an error page

    else:
        # Handle the case where the request method is not POST
        messages.error(request, 'Invalid request method. Expected POST.')

        # If you need to redirect to 'handle_multiple_alunos', add the necessary logic here
        return render(
            request,
            'app_certificado/pages/certificado/handle_multiple_alunos.html',
            {'certificado_data': certificado_data}
        )  # Render the page to let the user choose from the list of matching alunos



from django.shortcuts import get_object_or_404

def salvar_certificado(request):
    if request.method == 'POST':
        certificado_id = request.POST.get('certificado_id')
        aluno_id = request.POST.get('aluno_id')
        
        # Retrieve the stored data from the session
        certificado_data = request.session.get('certificado_data', {})
        
        print(f'certificado_id: {certificado_id}, aluno_id: {aluno_id}')
        print(f'certificado_data: {certificado_data}')

        # You may want to validate certificado_data here

        certificado = Certificado()
            
        # Update Certificado fields
        certificado.instituicao = certificado_data['instituicao']
        certificado.nome = certificado_data['nome']
        certificado.duracao = certificado_data['duracao']
        certificado.categoria = certificado_data['categoria']
        
        template_id = certificado_data.get('template')
        template = get_object_or_404(Template, pk=template_id)
        certificado.template = template
            
        # Convert aluno_id to an integer
        aluno_id = int(aluno_id)

        # Associate the Aluno instance with the certificado
        try:
            aluno = get_object_or_404(Aluno, pk=aluno_id)
        except Aluno.DoesNotExist:
            messages.error(request, 'Aluno not found with the provided ID.')
            return redirect('app_certificado:error_page')  # Redirect to an error page

        certificado.aluno = aluno

        # Save or update Certificado to the database
        certificado.save()

        return redirect('app_certificado:sucesso')  # Redirect to the success page

    else:
        messages.error(request, 'Invalid request method. Expected POST.')
        return redirect('app_certificado:error_page')  # Redirect to an error page




def error_page(request):
    return render(request, 'app_certificado/pages/certificado/error_page.html')  # Adjust the template path as needed



@login_required(login_url='app_certificado:login', redirect_field_name='next')
def activate_certificado(request, certificado_id):
    certificado = get_object_or_404(Certificado, pk=certificado_id)
    
    if request.method == 'POST':
        certificado.status = True
        certificado.save()
    
    return redirect('app_certificado:dashboard')

def sucesso(request):
    return render(request, 'app_certificado/pages/certificado/sucesso.html')

@user_passes_test(is_staff, login_url='app_certificado:login', redirect_field_name='next')
def lista_certificados(request):
    certificados = Certificado.objects.all()
    return render(request, 'app_certificado/pages/certificado/lista_certificados.html', {'certificados': certificados})

@user_passes_test(is_staff, login_url='app_certificado:login', redirect_field_name='next')
def criar_certificado(request):
    if request.method == 'POST':
        form = CertificadoFormCriar(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('app_certificado:lista_certificados')
    else:
        form = CertificadoFormCriar()
    return render(request, 'app_certificado/pages/certificado/criar_certificado.html', {'form': form})

@user_passes_test(is_staff, login_url='app_certificado:login', redirect_field_name='next')
def ver_certificado(request, certificado_id):
    certificado = get_object_or_404(Certificado, id=certificado_id)
    return render(request, 'app_certificado/pages/certificado/ver_certificado.html', {'certificado': certificado})

@user_passes_test(is_staff, login_url='app_certificado:login', redirect_field_name='next')
def atualizar_certificado(request, certificado_id):
    certificado = get_object_or_404(Certificado, id=certificado_id)
    if request.method == 'POST':
        form = CertificadoFormCriar(request.POST, request.FILES, instance=certificado)
        if form.is_valid():
            form.save()
            return redirect('app_certificado:lista_certificados')
    else:
        form = CertificadoFormCriar(instance=certificado)
    return render(request, 'app_certificado/pages/certificado/atualizar_certificado.html', {'form': form})

@user_passes_test(is_staff, login_url='app_certificado:login', redirect_field_name='next')
def excluir_certificado(request, certificado_id):
    certificado = get_object_or_404(Certificado, id=certificado_id)
    if request.method == 'POST':
        certificado.delete()
        return redirect('app_certificado:lista_certificados')
    return render(request, 'app_certificado/pages/certificado/excluir_certificado.html', {'certificado': certificado})


#SEARCH--------------------------------------------------
def search(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()
    
    certificado = Certificado.objects.filter(
        Q(nome__contains=search_term) |
        Q(instituicao__contains=search_term) |
        Q(duracao__contains=search_term) |
        Q(categoria__contains=search_term),
    ).order_by('-id')

    return render(request, 'app_certificado/pages/search.html', {
        'page_title': f'Search for "{search_term}"',
        'certificados': certificado,
    })

def search_alunos(request):
    search_term = request.GET.get('q', '').strip()
    search_type = request.GET.get('type', '')  # Obtém o tipo de pesquisa (ativos, inativos, todos)

    if search_type == 'todos':
        if not search_term:
            alunos = Aluno.objects.all()  # Busca todos os alunos, ativos e inativos
        else:
            alunos = Aluno.objects.filter(Q(nome__icontains=search_term) |
        Q(horas__contains=search_term))
    elif search_type == 'inativos':
        alunos = Aluno.objects.filter(Q(nome__icontains=search_term, status=True) |
        Q(horas__contains=search_term))
    elif search_type == 'ativos':
        alunos = Aluno.objects.filter(Q(nome__icontains=search_term, status=False) |
        Q(horas__contains=search_term))
    else:
        raise Http404()

    return render(request, 'app_certificado/pages/aluno/lista_alunos.html', {
        'page_title': f'Search for "{search_term}"',
        'alunos': alunos,
    })


def search_certificados(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()
    
    certificados = Certificado.objects.filter(
        Q(nome__contains=search_term) |
        Q(instituicao__contains=search_term) |
        Q(duracao__contains=search_term) |
        Q(categoria__contains=search_term),
    ).order_by('-id')

    return render(request, 'app_certificado/pages/certificado/lista_certificados.html', {
        'page_title': f'Search for "{search_term}"',
        'certificados': certificados,
    })

def search_usuarios(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()
    
    usuarios = User.objects.filter(
        Q(username__contains=search_term) | Q(email__contains=search_term)
    ).order_by('-id')

    return render(request, 'app_certificado/pages/user/user_list.html', {
        'page_title': f'Search for "{search_term}"',
        'users': usuarios,
    })

def search_templates(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()
    
    templates = Template.objects.filter(
        Q(instituicao__contains=search_term)
    ).order_by('-id')

    return render(request, 'app_certificado/pages/templateCertificado/lista_templates.html', {
        'page_title': f'Search for "{search_term}"',
        'templates': templates,
    })
#-----------------------------------------------------------------------------------------------------------------------------------