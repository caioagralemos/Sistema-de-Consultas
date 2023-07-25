from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User

from paciente.helpers.checar_cpf_valido import checar_cpf_valido
from paciente.helpers.checar_nome_valido import checar_nome_valido

from .models import Paciente

# Create your views here.

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        nome = f'{first_name} {last_name}'.strip()
        
        cpf = request.POST['cpf'].replace('-', '').replace('.', '').strip()

        if 'aftas' in request.POST:
            aftas = True
        else:
            aftas = False

        if 'consulta' in request.POST:
            consulta = True
        else:
            consulta = False

        if 'pos_cirurgia' in request.POST:
            pos_cirurgia = True
        else:
            pos_cirurgia = False

        if 'hipersensibilidade' in request.POST:
            hipersensibilidade = True
        else:
            hipersensibilidade = False

        if 'nevralgia' in request.POST:
            nevralgia = True
        else:
            nevralgia = False

        if 'lesoes' in request.POST:
            lesoes = True
        else:
            lesoes = False

        if password != password2:
            print('Senhas diferentes!')
            return redirect('register')
        elif not User.objects.filter(username=username).exists:
            print('Usuário já registrado!')
            return redirect('register')
        elif checar_nome_valido(nome) is False:
            print('Nome inválido!')
            return redirect('register')
        elif checar_cpf_valido(cpf) is False:
            print('CPF inválido!')
            return redirect('register')
        else:
            # Criando um novo usuário
            user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
            user.save()

            # Criando o perfil estendido vinculado ao usuário
            paciente = Paciente.objects.create(user=user, cpf=cpf, aftas=aftas, hipersensibilidade=hipersensibilidade, consulta=consulta, lesoes=lesoes, nevralgia=nevralgia, pos_cirurgia=pos_cirurgia)
            paciente.save()
            return redirect('login')
    else:
        return render(request, 'paciente/register.html')   

def dashboard(request):
    return render(request, 'paciente/dashboard.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
    
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            print('Something went wrong. Check your credentials and try again')
            return redirect('login')
    else:
        return render(request, 'paciente/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        print('You are now logged out!')
        return redirect('index')