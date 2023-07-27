from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError

from medico.models import Medico
from datas.models import Data
from consultas.models import Consulta

# Create your views here.

def agendar_consulta(request):
    if request.method == 'POST':
        paciente = request.user.paciente

        servico = request.POST['servico']
        if servico == 'Escolha seu serviço':
            messages.error(request, 'Você não escolheu o seu serviço!')
            return redirect('agendarconsulta')
        
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
            consulta = Consulta.objects.create(paciente=paciente, servico=servico, medico=medico, data=data)
            consulta.save()
        except:
            messages.error(request, 'Algo deu errado :/ Tente novamente')
            return redirect('agendarconsulta')
        

        messages.success(request, f'{paciente} com {medico.nome_completo} para tratar {servico} - dia {dia}/{mes}/{ano}')
        return redirect('dashboard')
    else:
        context = {
            'medicos': Medico.objects.all(),
        }
        return render(request, 'consultas/marcar_consulta.html', context)

def confirmacao(request):
    return render(request, 'consultas/confirmacao.html')