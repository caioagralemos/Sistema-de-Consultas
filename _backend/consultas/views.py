from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError

from medico.models import Medico
from datas.models import Data
from consultas.models import Consulta

from consultas.helpers.check_future import check_future
from consultas.helpers.consulta_render_error import consulta_render_error
from .choices import time_choices

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
            return consulta_render_error(request, 'Você não escolheu seu horário!', medico_user, data, horario)
        hora = int(horario[0:2])
        minuto = int(horario[2:])

        try:
            nova_data = Data.objects.create(ano=ano, mes=mes, dia=dia, hora=hora, minuto=minuto)
            nova_data.clean()
            nova_data.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
            return consulta_render_error(request, error_messages, medico_user, data, horario)
        
        if Consulta.objects.all().filter(medico=medico, data__dia=dia, data__mes=mes, data__ano=ano, data__hora=hora, data__minuto=minuto).exists():
            message = f'Data inválida: {nova_data}, esse médico já tem compromisso para esse horário.'
            return consulta_render_error(request, message, medico_user, data, horario)
        
        try:
            consulta = Consulta.objects.create(paciente=paciente, servico='consulta', medico=medico, data=nova_data)
            consulta.save()
        except:
            consulta_render_error(request, 'Algo deu errado :/ Tente novamente', medico_user, data, horario)
        

        messages.success(request, f'Consulta: {paciente} com {medico.nome_completo} - dia {dia}/{mes}/{ano} às {hora}:{minuto}')
        return redirect('dashboard')
    else:
        context = {
            'horarios': time_choices,
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
        
        data_1 = request.POST['data1']
        ano_1 = int(data_1[0:4])
        mes_1 = int(data_1[5:7])
        dia_1 = int(data_1[8:])
        horario_1 = request.POST['horario1']
        hora_1 = int(horario_1[0:2])
        minuto_1 = int(horario_1[2:])

        data_2 = request.POST['data1']
        ano_2 = int(data_2[0:4])
        mes_2 = int(data_2[5:7])
        dia_2 = int(data_2[8:])
        horario_2 = request.POST['horario2']
        hora_2 = int(horario_2[0:2])
        minuto_2 = int(horario_2[2:])

        data_3 = request.POST['data1']
        ano_3 = int(data_3[0:4])
        mes_3 = int(data_3[5:7])
        dia_3 = int(data_3[8:])
        horario_3 = request.POST['horario2']
        hora_3 = int(horario_3[0:2])
        minuto_3 = int(horario_3[2:])

        data_4 = request.POST['data1']
        ano_4 = int(data_4[0:4])
        mes_4 = int(data_4[5:7])
        dia_4 = int(data_4[8:])
        horario_4 = request.POST['horario2']
        hora_4 = int(horario_4[0:2])
        minuto_4 = int(horario_4[2:])

        if horario_1 == 'Escolha o horário':
            messages.error(request, 'Você não escolheu seu horário!')
            return redirect('aftas')
        
        if horario_2 == 'Escolha o horário':
            messages.error(request, 'Você não escolheu seu horário!')
            return redirect('aftas')

        if horario_3 == 'Escolha o horário':
            messages.error(request, 'Você não escolheu seu horário!')
            return redirect('aftas')
        
        if horario_4 == 'Escolha o horário':
            messages.error(request, 'Você não escolheu seu horário!')
            return redirect('aftas')        
        
        try:
            nova_data_1 = Data.objects.create(ano=ano_1, mes=mes_1, dia=dia_1, hora=hora_1, minuto=minuto_1)
            nova_data_1.clean()
            nova_data_1.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
            messages.error(request, f'Data inválida: {error_messages}')
            return redirect('aftas')

        try:
            nova_data_2 = Data.objects.create(ano=ano_2, mes=mes_2, dia=dia_2, hora=hora_2, minuto=minuto_2)
            nova_data_2.clean()
            nova_data_2.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
            messages.error(request, f'Data inválida: {error_messages}')
            return redirect('aftas')

        try:
            nova_data_3 = Data.objects.create(ano=ano_3, mes=mes_3, dia=dia_3, hora=hora_3, minuto=minuto_3)
            nova_data_3.clean()
            nova_data_3.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
            messages.error(request, f'Data inválida: {error_messages}')
            return redirect('aftas')

        try:
            nova_data_4 = Data.objects.create(ano=ano_4, mes=mes_4, dia=dia_4, hora=hora_4, minuto=minuto_4)
            nova_data_4.clean()
            nova_data_4.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
            messages.error(request, f'Data inválida: {error_messages}')
            return redirect('aftas')
        
        if check_future(nova_data_1, nova_data_2) not in range(4,9):
            messages.error(request, 'A diferença entre as sessões precisa ser entre 4 a 8 dias. Cheque a diferença entre as sessões 1 e 2.')
            return redirect('aftas')        
        elif check_future(nova_data_2, nova_data_3) not in range(4,9):
            messages.error(request, 'A diferença entre as sessões precisa ser entre 4 a 8 dias. Cheque a diferença entre as sessões 2 e 3.')
            return redirect('aftas')        
        elif check_future(nova_data_3, nova_data_4) not in range(4,9):
            messages.error(request, 'A diferença entre as sessões precisa ser entre 4 a 8 dias. Cheque a diferença entre as sessões 3 e 4.')
            return redirect('aftas')

        if Consulta.objects.filter(medico=medico, data__dia=dia_1, data__mes=mes_1, data__ano=ano_1, data__hora=hora_1, data__minuto=minuto_1).exists():
            messages.error(request, f'Data 1 inválida: {nova_data_1}, esse médico já tem compromisso para esse horário.')
            return redirect('aftas')
        
        if Consulta.objects.filter(medico=medico, data__dia=dia_2, data__mes=mes_2, data__ano=ano_2, data__hora=hora_2, data__minuto=minuto_2).exists():
            messages.error(request, f'Data 2 inválida: {nova_data_2}, esse médico já tem compromisso para esse horário.')
            return redirect('aftas')
        
        if Consulta.objects.filter(medico=medico, data__dia=dia_3, data__mes=mes_3, data__ano=ano_3, data__hora=hora_3, data__minuto=minuto_3).exists():
            messages.error(request, f'Data 3 inválida: {nova_data_3}, esse médico já tem compromisso para esse horário.')
            return redirect('aftas')
        
        if Consulta.objects.filter(medico=medico, data__dia=dia_4, data__mes=mes_4, data__ano=ano_4, data__hora=hora_4, data__minuto=minuto_4).exists():
            messages.error(request, f'Data 4 inválida: {nova_data_4}, esse médico já tem compromisso para esse horário.')
            return redirect('aftas')
        
        try:
            consulta = Consulta.objects.create(paciente=paciente, servico='aftas', medico=medico, data=nova_data_1)
            consulta.save()
            consulta2 = Consulta.objects.create(paciente=paciente, servico='aftas', medico=medico, data=nova_data_2)
            consulta2.save()
            consulta3 = Consulta.objects.create(paciente=paciente, servico='aftas', medico=medico, data=nova_data_3)
            consulta3.save()
            consulta4 = Consulta.objects.create(paciente=paciente, servico='aftas', medico=medico, data=nova_data_4)
            consulta4.save()
        except:
            messages.error(request, 'Algo deu errado :/ Tente novamente')
            return redirect('aftas')
        
        messages.success(request, f'Tratamento de Aftas: {paciente} com {medico.nome_completo} - Marcado com sucesso')
        return redirect('dashboard')
    else:
        context = {
                'horarios': time_choices,
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
                'horarios': time_choices,
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
            'horarios': time_choices,
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
            'horarios': time_choices,
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
            'horarios': time_choices,
            'medicos': Medico.objects.all().filter(lesoes=True),
        }
        return render(request, 'consultas/lesoes.html', context)