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

        horario = request.POST['horario']
        if horario == 'Escolha o horário':
            messages.error(request, 'Você não escolheu seu horário!')
            return redirect('agendarconsulta')
        hora = int(horario[0:2])
        minuto = int(horario[2:])

        try:
            nova_data = Data.objects.create(ano=ano, mes=mes, dia=dia, hora=hora, minuto=minuto)
            nova_data.clean()
            nova_data.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
            messages.error(request, f'Data inválida: {error_messages}')
            return redirect('agendarconsulta')
        
        if Consulta.objects.all().filter(medico=medico, data__dia=dia, data__mes=mes, data__ano=ano, data__hora=hora, data__minuto=minuto).exists():
            messages.error(request, f'Data inválida: {nova_data}, esse médico já tem compromisso para esse horário.')
            return redirect('agendarconsulta')
        
        try:
            consulta = Consulta.objects.create(paciente=paciente, servico='consulta', medico=medico, data=nova_data)
            consulta.save()
        except:
            messages.error(request, 'Algo deu errado :/ Tente novamente')
            return redirect('agendarconsulta')
        

        messages.success(request, f'Consulta: {paciente} com {medico.nome_completo} - dia {dia}/{mes}/{ano} às {hora}:{minuto}')
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
            return redirect('aftas')
        medico = Medico.objects.get(user__username=medico_user)
        
        data = request.POST['data']
        ano = int(data[0:4])
        mes = int(data[5:7])
        dia = int(data[8:])

        horario = request.POST['horario']
        if horario == 'Escolha o horário':
            messages.error(request, 'Você não escolheu seu horário!')
            return redirect('aftas')
        hora = int(horario[0:2])
        minuto = int(horario[2:])

        try:
            nova_data = Data.objects.create(ano=ano, mes=mes, dia=dia, hora=hora, minuto=minuto)
            nova_data.clean()
            nova_data.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
            messages.error(request, f'Data inválida: {error_messages}')
            return redirect('aftas')
        
        if Consulta.objects.filter(medico=medico, data__dia=dia, data__mes=mes, data__ano=ano, data__hora=hora, data__minuto=minuto).exists():
            messages.error(request, f'Data inválida: {nova_data}, esse médico já tem compromisso para esse horário.')
            return redirect('aftas')
        
        try:
            consulta = Consulta.objects.create(paciente=paciente, servico='aftas', medico=medico, data=nova_data)
            consulta.save()
        except:
            messages.error(request, 'Algo deu errado :/ Tente novamente')
            return redirect('aftas')
        

        messages.success(request, f'Tratamento de Aftas: {paciente} com {medico.nome_completo} - dia {dia}/{mes}/{ano} às {hora}:{minuto}')
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
            return redirect('hipersensibilidade')
        medico = Medico.objects.get(user__username=medico_user)
        
        data = request.POST['data']
        ano = int(data[0:4])
        mes = int(data[5:7])
        dia = int(data[8:])

        horario = request.POST['horario']
        if horario == 'Escolha o horário':
            messages.error(request, 'Você não escolheu seu horário!')
            return redirect('hipersensibilidade')
        hora = int(horario[0:2])
        minuto = int(horario[2:])

        try:
            nova_data = Data.objects.create(ano=ano, mes=mes, dia=dia, hora=hora, minuto=minuto)
            nova_data.clean()
            nova_data.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
            messages.error(request, f'Data inválida: {error_messages}')
            return redirect('hipersensibilidade')
        
        if Consulta.objects.filter(medico=medico, data__dia=dia, data__mes=mes, data__ano=ano, data__hora=hora, data__minuto=minuto).exists():
            messages.error(request, f'Data inválida: {nova_data}, esse médico já tem compromisso para esse horário.')
            return redirect('hipersensibilidade')        
        
        try:
            consulta = Consulta.objects.create(paciente=paciente, servico='hipersensibilidade', medico=medico, data=nova_data)
            consulta.save()
        except:
            messages.error(request, 'Algo deu errado :/ Tente novamente')
            return redirect('hipersensibilidade')
        

        messages.success(request, f'Tratamento de Hipersensibilidade: {paciente} com {medico.nome_completo} - dia {dia}/{mes}/{ano} às {hora}:{minuto}')
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
            return redirect('pos_cirurgia')
        medico = Medico.objects.get(user__username=medico_user)
        
        data = request.POST['data']
        ano = int(data[0:4])
        mes = int(data[5:7])
        dia = int(data[8:])

        horario = request.POST['horario']
        if horario == 'Escolha o horário':
            messages.error(request, 'Você não escolheu seu horário!')
            return redirect('pos_cirurgia')
        hora = int(horario[0:2])
        minuto = int(horario[2:])

        try:
            nova_data = Data.objects.create(ano=ano, mes=mes, dia=dia, hora=hora, minuto=minuto)
            nova_data.clean()
            nova_data.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
            messages.error(request, f'Data inválida: {error_messages}')
            return redirect('pos_cirurgia')
        
        if Consulta.objects.filter(medico=medico, data__dia=dia, data__mes=mes, data__ano=ano, data__hora=hora, data__minuto=minuto).exists():
            messages.error(request, f'Data inválida: {nova_data}, esse médico já tem compromisso para esse horário.')
            return redirect('pos_cirurgia')

        try:
            consulta = Consulta.objects.create(paciente=paciente, servico='pos_cirurgia', medico=medico, data=nova_data)
            consulta.save()
        except:
            messages.error(request, 'Algo deu errado :/ Tente novamente')
            return redirect('pos_cirurgia')
        

        messages.success(request, f'Acompanhamento Pós-Cirúrgico: {paciente} com {medico.nome_completo} - dia {dia}/{mes}/{ano} às {hora}:{minuto}')
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
            return redirect('nevralgia')
        medico = Medico.objects.get(user__username=medico_user)
        
        data = request.POST['data']
        ano = int(data[0:4])
        mes = int(data[5:7])
        dia = int(data[8:])

        horario = request.POST['horario']
        if horario == 'Escolha o horário':
            messages.error(request, 'Você não escolheu seu horário!')
            return redirect('nevralgia')
        hora = int(horario[0:2])
        minuto = int(horario[2:])        

        try:
            nova_data = Data.objects.create(ano=ano, mes=mes, dia=dia, hora=hora, minuto=minuto)
            nova_data.clean()
            nova_data.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
            messages.error(request, f'Data inválida: {error_messages}')
            return redirect('nevralgia')

        if Consulta.objects.filter(medico=medico, data__dia=dia, data__mes=mes, data__ano=ano, data__hora=hora, data__minuto=minuto).exists():
            messages.error(request, f'Data inválida: {nova_data}, esse médico já tem compromisso para esse horário.')
            return redirect('nevralgia')
                
        try:
            consulta = Consulta.objects.create(paciente=paciente, servico='nevralgia', medico=medico, data=nova_data)
            consulta.save()
        except:
            messages.error(request, 'Algo deu errado :/ Tente novamente')
            return redirect('nevralgia')
        

        messages.success(request, f'Tratamento de Nevralgia: {paciente} com {medico.nome_completo} - dia {dia}/{mes}/{ano} às {hora}:{minuto}')
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

        horario = request.POST['horario']
        if horario == 'Escolha o horário':
            messages.error(request, 'Você não escolheu seu horário!')
            return redirect('lesoes')
        hora = int(horario[0:2])
        minuto = int(horario[2:])        

        try:
            nova_data = Data.objects.create(ano=ano, mes=mes, dia=dia, hora=hora, minuto=minuto)
            nova_data.clean()
            nova_data.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
            messages.error(request, f'Data inválida: {error_messages}')
            return redirect('lesoes')
        
        if Consulta.objects.filter(medico=medico, data__dia=dia, data__mes=mes, data__ano=ano, data__hora=hora, data__minuto=minuto).exists():
            messages.error(request, f'Data inválida: {nova_data}, esse médico já tem compromisso para esse horário.')
            return redirect('lesoes')
        
        try:
            consulta = Consulta.objects.create(paciente=paciente, servico='lesoes', medico=medico, data=nova_data)
            consulta.save()
        except:
            messages.error(request, 'Algo deu errado :/ Tente novamente')
            return redirect('lesoes')
        

        messages.success(request, f'Tratamento de Lesões: {paciente} com {medico.nome_completo} - dia {dia}/{mes}/{ano} às {hora}:{minuto}')
        return redirect('dashboard')
    else:
        context = {
            'medicos': Medico.objects.all().filter(lesoes=True),
        }
        return render(request, 'consultas/lesoes.html', context)