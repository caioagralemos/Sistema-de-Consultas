from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError

from medico.models import Medico
from datas.models import Data
from consultas.models import Consulta

# Create your views here.

def consulta(request):
    if request.method == 'POST':
        paciente = request.user.paciente
        
        medico_user = request.POST['medico']
        if medico_user == 'Escolha seu médico':
            messages.error(request, 'Você não escolheu o seu médico!')
            return redirect('agendarconsulta')
        medico = Medico.objects.get(user__username=medico_user)
        
        data = request.POST['data']
        ano = int(data[0:4])
        mes = int(data[5:7])
        dia = int(data[8:])

        try:
            data = Data.objects.create(ano=ano, mes=mes, dia=dia)
            data.clean()
            data.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
            messages.error(request, f'Data inválida: {error_messages}')
            return redirect('agendarconsulta')
        
        horario = request.POST['horario']
        if horario == 'Escolha o horário':
            messages.error(request, 'Você não escolheu seu horário!')
            return redirect('agendarconsulta')
        
        try:
            consulta = Consulta.objects.create(paciente=paciente, servico='consulta', medico=medico, data=data)
            consulta.save()
        except:
            messages.error(request, 'Algo deu errado :/ Tente novamente')
            return redirect('agendarconsulta')
        

        messages.success(request, f'Consulta: {paciente} com {medico.nome_completo} - dia {dia}/{mes}/{ano}')
        return redirect('dashboard')
    else:
        context = {
            'medicos': Medico.objects.all().filter(consulta=True),
        }
        return render(request, 'consultas/marcar_consulta.html', context)

def aftas(request):
    if request.method == 'POST':
        paciente = request.user.paciente
        
        medico_user = request.POST['medico']
        if medico_user == 'Escolha seu médico':
            messages.error(request, 'Você não escolheu o seu médico!')
            return redirect('agendarconsulta')
        medico = Medico.objects.get(user__username=medico_user)
        
        data = request.POST['data']
        ano = int(data[0:4])
        mes = int(data[5:7])
        dia = int(data[8:])

        try:
            data = Data.objects.create(ano=ano, mes=mes, dia=dia)
            data.clean()
            data.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
            messages.error(request, f'Data inválida: {error_messages}')
            return redirect('agendarconsulta')
        
        horario = request.POST['horario']
        if horario == 'Escolha o horário':
            messages.error(request, 'Você não escolheu seu horário!')
            return redirect('agendarconsulta')
        
        try:
            consulta = Consulta.objects.create(paciente=paciente, servico='aftas', medico=medico, data=data)
            consulta.save()
        except:
            messages.error(request, 'Algo deu errado :/ Tente novamente')
            return redirect('agendarconsulta')
        

        messages.success(request, f'Tratamento de Aftas: {paciente} com {medico.nome_completo} - dia {dia}/{mes}/{ano}')
        return redirect('dashboard')
    else:
        context = {
                'medicos': Medico.objects.all().filter(aftas=True),
            }
        return render(request, 'consultas/aftas.html', context)

def hipersensibilidade(request):
    if request.method == 'POST':
        paciente = request.user.paciente
        
        medico_user = request.POST['medico']
        if medico_user == 'Escolha seu médico':
            messages.error(request, 'Você não escolheu o seu médico!')
            return redirect('agendarconsulta')
        medico = Medico.objects.get(user__username=medico_user)
        
        data = request.POST['data']
        ano = int(data[0:4])
        mes = int(data[5:7])
        dia = int(data[8:])

        try:
            data = Data.objects.create(ano=ano, mes=mes, dia=dia)
            data.clean()
            data.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
            messages.error(request, f'Data inválida: {error_messages}')
            return redirect('agendarconsulta')
        
        horario = request.POST['horario']
        if horario == 'Escolha o horário':
            messages.error(request, 'Você não escolheu seu horário!')
            return redirect('agendarconsulta')
        
        try:
            consulta = Consulta.objects.create(paciente=paciente, servico='hipersensibilidade', medico=medico, data=data)
            consulta.save()
        except:
            messages.error(request, 'Algo deu errado :/ Tente novamente')
            return redirect('agendarconsulta')
        

        messages.success(request, f'Tratamento de Hipersensibilidade: {paciente} com {medico.nome_completo} - dia {dia}/{mes}/{ano}')
        return redirect('dashboard')
    else:
        context = {
                'medicos': Medico.objects.all().filter(hipersensibilidade=True),
            }
        return render(request, 'consultas/hipersensibilidade.html', context)

def pos_cirurgia(request):
    if request.method == 'POST':
        paciente = request.user.paciente
        
        medico_user = request.POST['medico']
        if medico_user == 'Escolha seu médico':
            messages.error(request, 'Você não escolheu o seu médico!')
            return redirect('agendarconsulta')
        medico = Medico.objects.get(user__username=medico_user)
        
        data = request.POST['data']
        ano = int(data[0:4])
        mes = int(data[5:7])
        dia = int(data[8:])

        try:
            data = Data.objects.create(ano=ano, mes=mes, dia=dia)
            data.clean()
            data.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
            messages.error(request, f'Data inválida: {error_messages}')
            return redirect('agendarconsulta')
        
        horario = request.POST['horario']
        if horario == 'Escolha o horário':
            messages.error(request, 'Você não escolheu seu horário!')
            return redirect('agendarconsulta')
        
        try:
            consulta = Consulta.objects.create(paciente=paciente, servico='pos_cirurgia', medico=medico, data=data)
            consulta.save()
        except:
            messages.error(request, 'Algo deu errado :/ Tente novamente')
            return redirect('agendarconsulta')
        

        messages.success(request, f'Acompanhamento Pós-Cirúrgico: {paciente} com {medico.nome_completo} - dia {dia}/{mes}/{ano}')
        return redirect('dashboard')
    else:
        context = {
            'medicos': Medico.objects.all().filter(pos_cirurgia=True),
            }
        return render(request, 'consultas/pos_cirurgia.html', context)

def nevralgia(request):
    if request.method == 'POST':
        paciente = request.user.paciente
        
        medico_user = request.POST['medico']
        if medico_user == 'Escolha seu médico':
            messages.error(request, 'Você não escolheu o seu médico!')
            return redirect('agendarconsulta')
        medico = Medico.objects.get(user__username=medico_user)
        
        data = request.POST['data']
        ano = int(data[0:4])
        mes = int(data[5:7])
        dia = int(data[8:])

        try:
            data = Data.objects.create(ano=ano, mes=mes, dia=dia)
            data.clean()
            data.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
            messages.error(request, f'Data inválida: {error_messages}')
            return redirect('agendarconsulta')
        
        horario = request.POST['horario']
        if horario == 'Escolha o horário':
            messages.error(request, 'Você não escolheu seu horário!')
            return redirect('agendarconsulta')
        
        try:
            consulta = Consulta.objects.create(paciente=paciente, servico='nevralgia', medico=medico, data=data)
            consulta.save()
        except:
            messages.error(request, 'Algo deu errado :/ Tente novamente')
            return redirect('agendarconsulta')
        

        messages.success(request, f'Tratamento de Nevralgia: {paciente} com {medico.nome_completo} - dia {dia}/{mes}/{ano}')
        return redirect('dashboard')
    else:
        context = {
            'medicos': Medico.objects.all().filter(nevralgia=True),
        }
        return render(request, 'consultas/nevralgia.html', context)

def lesoes(request):
    if request.method == 'POST':
        paciente = request.user.paciente
        
        medico_user = request.POST['medico']
        if medico_user == 'Escolha seu médico':
            messages.error(request, 'Você não escolheu o seu médico!')
            return redirect('agendarconsulta')
        medico = Medico.objects.get(user__username=medico_user)
        
        data = request.POST['data']
        ano = int(data[0:4])
        mes = int(data[5:7])
        dia = int(data[8:])

        try:
            data = Data.objects.create(ano=ano, mes=mes, dia=dia)
            data.clean()
            data.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
            messages.error(request, f'Data inválida: {error_messages}')
            return redirect('agendarconsulta')
        
        horario = request.POST['horario']
        if horario == 'Escolha o horário':
            messages.error(request, 'Você não escolheu seu horário!')
            return redirect('agendarconsulta')
        
        try:
            consulta = Consulta.objects.create(paciente=paciente, servico='lesoes', medico=medico, data=data)
            consulta.save()
        except:
            messages.error(request, 'Algo deu errado :/ Tente novamente')
            return redirect('agendarconsulta')
        

        messages.success(request, f'Tratamento de Lesões: {paciente} com {medico.nome_completo} - dia {dia}/{mes}/{ano}')
        return redirect('dashboard')
    else:
        context = {
            'medicos': Medico.objects.all().filter(lesoes=True),
        }
        return render(request, 'consultas/lesoes.html', context)