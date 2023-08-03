from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User

from paciente.helpers.checar_cpf_valido import checar_cpf_valido
from paciente.helpers.checar_nome_valido import checar_nome_valido

from .models import Paciente
from consultas.models import Consulta

# Create your views here.

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
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
            messages.error(request, 'Senhas diferentes!')
            return redirect('register')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Usuário já registrado!')
            return redirect('register')
        elif Paciente.objects.filter(cpf=cpf).exists():
            messages.error(request, 'CPF já registrado!')
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email já registrado!')
            return redirect('register')
        elif checar_nome_valido(nome) is False:
            messages.error(request, 'Nome inválido!')
            return redirect('register')
        elif checar_cpf_valido(cpf) is False:
            messages.error(request, 'CPF inválido!')
            return redirect('register')
        else:
            # Criando um novo usuário
            user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
            user.save()

            # Criando o perfil estendido vinculado ao usuário
            paciente = Paciente.objects.create(user=user, cpf=cpf, aftas=aftas, hipersensibilidade=hipersensibilidade, consulta=True, lesoes=lesoes, nevralgia=nevralgia, pos_cirurgia=pos_cirurgia)
            paciente.save()
            messages.success(request, f'Conta de {first_name} criada com sucesso!')
            return redirect('login')
    else:
        return render(request, 'paciente/register.html')   

def dashboard(request):
    context = {
        'consultas': Consulta.objects.filter(paciente=request.user.paciente, ehParte2=False).order_by('data__data_hora_completa'),
    }
    return render(request, 'paciente/dashboard.html', context)

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
    
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            try:
                if user.medico:
                    messages.success(request, f'Bem vindo(a), {user.medico.first_name}')
                    return redirect('medico-dashboard')
            except:
                messages.success(request, f'Bem vindo(a), {user.first_name}')
                return redirect('dashboard')
        else:
            messages.error(request, 'Algo deu errado. Reveja suas credenciais e tente novamente!')
            return redirect('login')
    else:
        return render(request, 'paciente/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'Você fez logout com sucesso!')
        return redirect('index')