from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.models import User, auth
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.conf import settings


def index(request):
    if request.user.is_authenticated:
        return render(request, 'registration/index.html')
    else:
        return redirect('login')


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Este nome de usuário já está em uso. Tente outro.')
                return HttpResponseRedirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email já cadastrado')
                return HttpResponseRedirect('register')
            else:
                user = User.objects.create_user(username=username, password=password,
                                                email=email, first_name=first_name, last_name=last_name)
                user.is_active = False
                user.save()
                # Mail system #
                subject = "Projeto UserAuth - Confirmação de cadastro"
                email_template_name = "registration/verify_email.txt"
                c = {
                    "email": user.email,
                    'domain': 'userauth-portal.herokuapp.com',
                    'site_name': 'Projeto UserAuth',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                    'protocol': 'https',
                }
                email = render_to_string(email_template_name, c)
                try:
                    send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
                except BadHeaderError:

                    return HttpResponse('Invalid header found.')

                messages.success(request, 'Te enviamos um email para validação da conta. Verifique seu email para '
                                          'ativá-la.')
                return HttpResponseRedirect('login')
        else:
            messages.info(request, 'As senhas não são iguais. Tente novamente.')
            return HttpResponseRedirect('register')
    else:
        return render(request, 'registration/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, f'Bem vindo, {username}.Você se autenticou com sucesso.')
            return redirect('index')
        else:
            messages.error(request, 'Senha ou usuário inválidos')
            return redirect('login')

    else:
        return render(request, 'registration/login.html')


def logout(request):
    auth.logout(request)
    messages.success(request, 'Você se desconectou com sucesso.')
    return HttpResponseRedirect('login')


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Projeto UserAuth - Recuperação de senha solicitada"
                    email_template_name = "password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': 'userauth-portal.herokuapp.com',
                        'site_name': 'Projeto UserAuth',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'https',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
                    except BadHeaderError:

                        return HttpResponse('Invalid header found.')

                    messages.success(request,
                                     'Um email instruções para redefinição de senha foi enviado para o email informado.')
                    return HttpResponseRedirect('login')
            messages.error(request, 'O email digitado é inválido.')
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password/password_reset.html",
                  context={"password_reset_form": password_reset_form})
