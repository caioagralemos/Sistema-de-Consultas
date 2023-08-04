from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError

from medico.models import Medico
from datas.models import Data
from consultas.models import Consulta

from .choices import time_choices
from consultas.helpers.check_future import check_future

from consultas.helpers.consulta_render_error import consulta_render_error
from consultas.helpers.aftas_render_error import aftas_render_error
from consultas.helpers.hipersensibilidade_render_error import hipersensibilidade_render_error
from consultas.helpers.lesoes_render_error import lesoes_render_error
from consultas.helpers.pos_cirurgia_render_error import pos_cirurgia_render_error
from consultas.helpers.nevralgia_render_error import nevralgia_render_error

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
            return consulta_render_error(request, 'Você não escolheu seu horário!', medico, data, horario)
        hora_1 = int(horario[0:2])
        minuto_1 = int(horario[2:])

        if hora_1 >= 20:
            return consulta_render_error(request, 'As consultas só vão até 20:30, portanto não é possível marcar consulta de 1h para 20h.', medico, data, horario)

        if minuto_1 == 30:
            minuto_2 = 0
            hora_2 = hora_1 + 1
        else:
            minuto_2 = 30
            hora_2 = hora_1

        try:
            nova_data_1 = Data.objects.create(ano=ano, mes=mes, dia=dia, hora=hora_1, minuto=minuto_1)
            nova_data_1.clean()
            nova_data_1.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
            return consulta_render_error(request, error_messages, medico, data, horario)
        
        try:
            nova_data_2 = Data.objects.create(ano=ano, mes=mes, dia=dia, hora=hora_2, minuto=minuto_2)
            nova_data_2.clean()
            nova_data_2.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
            return consulta_render_error(request, error_messages, medico, data, horario)
        
        if Consulta.objects.all().filter(medico=medico, data__dia=dia, data__mes=mes, data__ano=ano, data__hora=hora_1, data__minuto=minuto_1).exists():
            message = f'Data inválida: {nova_data_1}, esse médico já tem compromisso para esse horário.'
            return consulta_render_error(request, message, medico, data, horario)
        
        if Consulta.objects.all().filter(medico=medico, data__dia=dia, data__mes=mes, data__ano=ano, data__hora=hora_2, data__minuto=minuto_2).exists():
            message = f'Data inválida: {nova_data_1}, esse médico já tem compromisso para esse horário.'
            return consulta_render_error(request, message, medico, data, horario)
        
        try:
            consulta = Consulta.objects.create(paciente=paciente, servico='consulta', medico=medico, data=nova_data_1)
            consulta.save()
            consulta2 = Consulta.objects.create(paciente=paciente, servico='consulta', medico=medico, data=nova_data_2, ehParte2=True)
            consulta2.save()
        except:
            consulta_render_error(request, 'Algo deu errado :/ Tente novamente', medico, data, horario)
        

        messages.success(request, f'Consulta: {paciente} com {medico.nome_completo} - dia {dia}/{mes}/{ano} às {hora_1}:{minuto_1}')
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
            return aftas_render_error(request, 'Você não escolheu seu médico!', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4)
        medico = Medico.objects.get(user__username=medico_user)
        
        data_1 = request.POST['data1']
        ano_1 = int(data_1[0:4])
        mes_1 = int(data_1[5:7])
        dia_1 = int(data_1[8:])
        horario_1 = request.POST['horario1']
        if horario_1 == 'Escolha o horário':
            return aftas_render_error(request, 'Você não escolheu seu horário 1!', medico, data_1, horario_1)
        hora_1 = int(horario_1[0:2])
        minuto_1 = int(horario_1[2:])

        data_2 = request.POST['data2']
        ano_2 = int(data_2[0:4])
        mes_2 = int(data_2[5:7])
        dia_2 = int(data_2[8:])
        horario_2 = request.POST['horario2']
        if horario_2 == 'Escolha o horário':
            return aftas_render_error(request, 'Você não escolheu seu horário 2!', medico, data_1, horario_1, data_2, horario_2)
        hora_2 = int(horario_2[0:2])
        minuto_2 = int(horario_2[2:])

        data_3 = request.POST['data3']
        ano_3 = int(data_3[0:4])
        mes_3 = int(data_3[5:7])
        dia_3 = int(data_3[8:])
        horario_3 = request.POST['horario3']
        if horario_3 == 'Escolha o horário':
            return aftas_render_error(request, 'Você não escolheu seu horário 3!', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3)
        hora_3 = int(horario_3[0:2])
        minuto_3 = int(horario_3[2:])

        data_4 = request.POST['data4']
        ano_4 = int(data_4[0:4])
        mes_4 = int(data_4[5:7])
        dia_4 = int(data_4[8:])
        horario_4 = request.POST['horario4']
        if horario_4 == 'Escolha o horário':
            return aftas_render_error(request, 'Você não escolheu seu horário 4!', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4)
        hora_4 = int(horario_4[0:2])
        minuto_4 = int(horario_4[2:])

        try:
            nova_data_1 = Data.objects.create(ano=ano_1, mes=mes_1, dia=dia_1, hora=hora_1, minuto=minuto_1)
            nova_data_1.clean()
            nova_data_1.save()
        except ValidationError as e:
            error_messages = 'Sessão 1: ' + ', '.join(e.messages)
            return aftas_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4)

        try:
            nova_data_2 = Data.objects.create(ano=ano_2, mes=mes_2, dia=dia_2, hora=hora_2, minuto=minuto_2)
            nova_data_2.clean()
            nova_data_2.save()
        except ValidationError as e:
            error_messages = 'Sessão 2: ' +', '.join(e.messages)
            return aftas_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4)

        try:
            nova_data_3 = Data.objects.create(ano=ano_3, mes=mes_3, dia=dia_3, hora=hora_3, minuto=minuto_3)
            nova_data_3.clean()
            nova_data_3.save()
        except ValidationError as e:
            error_messages = 'Sessão 3: ' + ', '.join(e.messages)
            return aftas_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4)

        try:
            nova_data_4 = Data.objects.create(ano=ano_4, mes=mes_4, dia=dia_4, hora=hora_4, minuto=minuto_4)
            nova_data_4.clean()
            nova_data_4.save()
        except ValidationError as e:
            error_messages = 'Sessão 4: ' + ', '.join(e.messages)
            return aftas_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4)
        
        if check_future(nova_data_1, nova_data_2) not in range(4,9):      
            return aftas_render_error(request, 'A diferença entre as sessões precisa ser entre 4 a 8 dias. Cheque a diferença entre as sessões 1 e 2.', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4)
        elif check_future(nova_data_2, nova_data_3) not in range(4,9):
            return aftas_render_error(request, 'A diferença entre as sessões precisa ser entre 4 a 8 dias. Cheque a diferença entre as sessões 2 e 3.', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4)    
        elif check_future(nova_data_3, nova_data_4) not in range(4,9):
            return aftas_render_error(request, 'A diferença entre as sessões precisa ser entre 4 a 8 dias. Cheque a diferença entre as sessões 3 e 4.', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4)

        if Consulta.objects.filter(medico=medico, data__dia=dia_1, data__mes=mes_1, data__ano=ano_1, data__hora=hora_1, data__minuto=minuto_1).exists():
            error_messages = f'Data 1 inválida: {nova_data_1}, esse médico já tem compromisso para esse horário.'
            return aftas_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4)
        
        if Consulta.objects.filter(medico=medico, data__dia=dia_2, data__mes=mes_2, data__ano=ano_2, data__hora=hora_2, data__minuto=minuto_2).exists():
            error_messages = f'Data 2 inválida: {nova_data_2}, esse médico já tem compromisso para esse horário.'
            return aftas_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4)
        
        if Consulta.objects.filter(medico=medico, data__dia=dia_3, data__mes=mes_3, data__ano=ano_3, data__hora=hora_3, data__minuto=minuto_3).exists():
            error_messages = f'Data 3 inválida: {nova_data_3}, esse médico já tem compromisso para esse horário.'
            return aftas_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4)
        
        if Consulta.objects.filter(medico=medico, data__dia=dia_4, data__mes=mes_4, data__ano=ano_4, data__hora=hora_4, data__minuto=minuto_4).exists():
            error_messages = f'Data 4 inválida: {nova_data_4}, esse médico já tem compromisso para esse horário.'
            return aftas_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4)
        
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
            error_messages = 'Algo deu errado :/ Tente novamente'
            return aftas_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4)
        
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
            return hipersensibilidade_render_error(request, 'Você não escolheu seu médico!', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6)
        medico = Medico.objects.get(user__username=medico_user)
        
        data_1 = request.POST['data1']
        ano_1 = int(data_1[0:4])
        mes_1 = int(data_1[5:7])
        dia_1 = int(data_1[8:])
        horario_1 = request.POST['horario1']
        if horario_1 == 'Escolha o horário':
            return hipersensibilidade_render_error(request, 'Você não escolheu seu horário 1!', medico, data_1, horario_1)
        hora_1 = int(horario_1[0:2])
        minuto_1 = int(horario_1[2:])

        data_2 = request.POST['data2']
        ano_2 = int(data_2[0:4])
        mes_2 = int(data_2[5:7])
        dia_2 = int(data_2[8:])
        horario_2 = request.POST['horario2']
        if horario_2 == 'Escolha o horário':
            return hipersensibilidade_render_error(request, 'Você não escolheu seu horário 2!', medico, data_1, horario_1, data_2, horario_2)
        hora_2 = int(horario_2[0:2])
        minuto_2 = int(horario_2[2:])

        data_3 = request.POST['data3']
        ano_3 = int(data_3[0:4])
        mes_3 = int(data_3[5:7])
        dia_3 = int(data_3[8:])
        horario_3 = request.POST['horario3']
        if horario_3 == 'Escolha o horário':
            return hipersensibilidade_render_error(request, 'Você não escolheu seu horário 3!', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3)
        hora_3 = int(horario_3[0:2])
        minuto_3 = int(horario_3[2:])

        data_4 = request.POST['data4']
        ano_4 = int(data_4[0:4])
        mes_4 = int(data_4[5:7])
        dia_4 = int(data_4[8:])
        horario_4 = request.POST['horario4']
        if horario_4 == 'Escolha o horário':
            return hipersensibilidade_render_error(request, 'Você não escolheu seu horário 4!', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4)
        hora_4 = int(horario_4[0:2])
        minuto_4 = int(horario_4[2:])

        data_5 = request.POST['data5']
        ano_5 = int(data_5[0:4])
        mes_5 = int(data_5[5:7])
        dia_5 = int(data_5[8:])
        horario_5 = request.POST['horario5']
        if horario_5 == 'Escolha o horário':
            return hipersensibilidade_render_error(request, 'Você não escolheu seu horário 5!', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5)        
        hora_5 = int(horario_5[0:2])
        minuto_5 = int(horario_5[2:])

        data_6 = request.POST['data6']
        ano_6 = int(data_6[0:4])
        mes_6 = int(data_6[5:7])
        dia_6 = int(data_6[8:])
        horario_6 = request.POST['horario6']
        if horario_6 == 'Escolha o horário':
            return hipersensibilidade_render_error(request, 'Você não escolheu seu horário 6!', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6)
        hora_6 = int(horario_6[0:2])
        minuto_6 = int(horario_6[2:])

        try:
            nova_data_1 = Data.objects.create(ano=ano_1, mes=mes_1, dia=dia_1, hora=hora_1, minuto=minuto_1)
            nova_data_1.clean()
            nova_data_1.save()
        except ValidationError as e:
            error_messages = 'Sessão 1: ' + ', '.join(e.messages)
            return hipersensibilidade_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6)

        try:
            nova_data_2 = Data.objects.create(ano=ano_2, mes=mes_2, dia=dia_2, hora=hora_2, minuto=minuto_2)
            nova_data_2.clean()
            nova_data_2.save()
        except ValidationError as e:
            error_messages = 'Sessão 2: ' + ', '.join(e.messages)
            return hipersensibilidade_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6)

        try:
            nova_data_3 = Data.objects.create(ano=ano_3, mes=mes_3, dia=dia_3, hora=hora_3, minuto=minuto_3)
            nova_data_3.clean()
            nova_data_3.save()
        except ValidationError as e:
            error_messages = 'Sessão 3: ' + ', '.join(e.messages)
            return hipersensibilidade_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6)

        try:
            nova_data_4 = Data.objects.create(ano=ano_4, mes=mes_4, dia=dia_4, hora=hora_4, minuto=minuto_4)
            nova_data_4.clean()
            nova_data_4.save()
        except ValidationError as e:
            error_messages = 'Sessão 4: ' + ', '.join(e.messages)
            return hipersensibilidade_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6)

        try:
            nova_data_5 = Data.objects.create(ano=ano_5, mes=mes_5, dia=dia_5, hora=hora_5, minuto=minuto_5)
            nova_data_5.clean()
            nova_data_5.save()
        except ValidationError as e:
            error_messages = 'Sessão 4: ' + ', '.join(e.messages)
            return hipersensibilidade_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6)

        try:
            nova_data_6 = Data.objects.create(ano=ano_6, mes=mes_6, dia=dia_6, hora=hora_6, minuto=minuto_6)
            nova_data_6.clean()
            nova_data_6.save()
        except ValidationError as e:
            error_messages = 'Sessão 6: ' + ', '.join(e.messages)
            return hipersensibilidade_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6)
        
        if check_future(nova_data_1, nova_data_2) not in range(15,31):      
            return hipersensibilidade_render_error(request, 'A diferença entre as sessões precisa ser entre 15 a 30 dias. Cheque a diferença entre as sessões 1 e 2.', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6)
        elif check_future(nova_data_2, nova_data_3) not in range(15,31):
            return hipersensibilidade_render_error(request, 'A diferença entre as sessões precisa ser entre 15 a 30 dias. Cheque a diferença entre as sessões 2 e 3.', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6)    
        elif check_future(nova_data_3, nova_data_4) not in range(15,31):
            return hipersensibilidade_render_error(request, 'A diferença entre as sessões precisa ser entre 15 a 30 dias. Cheque a diferença entre as sessões 3 e 4.', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6)
        elif check_future(nova_data_4, nova_data_5) not in range(15,31):
            return hipersensibilidade_render_error(request, 'A diferença entre as sessões precisa ser entre 15 a 30 dias. Cheque a diferença entre as sessões 4 e 5.', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6)
        elif check_future(nova_data_5, nova_data_6) not in range(15,31):
            return hipersensibilidade_render_error(request, 'A diferença entre as sessões precisa ser entre 15 a 30 dias. Cheque a diferença entre as sessões 5 e 6.', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6)

        if Consulta.objects.filter(medico=medico, data__dia=dia_1, data__mes=mes_1, data__ano=ano_1, data__hora=hora_1, data__minuto=minuto_1).exists():
            error_messages = f'Data 1 inválida: {nova_data_1}, esse médico já tem compromisso para esse horário.'
            return hipersensibilidade_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6)
        
        if Consulta.objects.filter(medico=medico, data__dia=dia_2, data__mes=mes_2, data__ano=ano_2, data__hora=hora_2, data__minuto=minuto_2).exists():
            error_messages = f'Data 2 inválida: {nova_data_2}, esse médico já tem compromisso para esse horário.'
            return hipersensibilidade_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6)
        
        if Consulta.objects.filter(medico=medico, data__dia=dia_3, data__mes=mes_3, data__ano=ano_3, data__hora=hora_3, data__minuto=minuto_3).exists():
            error_messages = f'Data 3 inválida: {nova_data_3}, esse médico já tem compromisso para esse horário.'
            return hipersensibilidade_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6)
        
        if Consulta.objects.filter(medico=medico, data__dia=dia_4, data__mes=mes_4, data__ano=ano_4, data__hora=hora_4, data__minuto=minuto_4).exists():
            error_messages = f'Data 4 inválida: {nova_data_4}, esse médico já tem compromisso para esse horário.'
            return hipersensibilidade_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6)
        
        if Consulta.objects.filter(medico=medico, data__dia=dia_5, data__mes=mes_5, data__ano=ano_5, data__hora=hora_5, data__minuto=minuto_5).exists():
            error_messages = f'Data 5 inválida: {nova_data_5}, esse médico já tem compromisso para esse horário.'
            return hipersensibilidade_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6)
        
        if Consulta.objects.filter(medico=medico, data__dia=dia_6, data__mes=mes_6, data__ano=ano_6, data__hora=hora_6, data__minuto=minuto_6).exists():
            error_messages = f'Data 6 inválida: {nova_data_6}, esse médico já tem compromisso para esse horário.'
            return hipersensibilidade_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6)
        
        try:
            consulta = Consulta.objects.create(paciente=paciente, servico='hipersensibilidade', medico=medico, data=nova_data_1)
            consulta.save()
            consulta2 = Consulta.objects.create(paciente=paciente, servico='hipersensibilidade', medico=medico, data=nova_data_2)
            consulta2.save()
            consulta3 = Consulta.objects.create(paciente=paciente, servico='hipersensibilidade', medico=medico, data=nova_data_3)
            consulta3.save()
            consulta4 = Consulta.objects.create(paciente=paciente, servico='hipersensibilidade', medico=medico, data=nova_data_4)
            consulta4.save()
            consulta5 = Consulta.objects.create(paciente=paciente, servico='hipersensibilidade', medico=medico, data=nova_data_5)
            consulta5.save()
            consulta6 = Consulta.objects.create(paciente=paciente, servico='hipersensibilidade', medico=medico, data=nova_data_6)
            consulta6.save()
        except:
            error_messages = 'Algo deu errado :/ Tente novamente'
            return hipersensibilidade_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6)
        
        messages.success(request, f'Tratamento de hipersensibilidade: {paciente} com {medico.nome_completo} - Marcado com sucesso')
        return redirect('dashboard')
    else:
        context = {
                'horarios': time_choices,
                'medicos': Medico.objects.all().filter(hipersensibilidade=True),
            }
        return render(request, 'consultas/hipersensibilidade.html', context)
    
def lesoes(request):
    if request.method == 'POST':
        paciente = request.user.paciente
        
        medico_user = request.POST['medico']
        if medico_user == 'Escolha seu médico':
            return lesoes_render_error(request, 'Você não escolheu seu médico!', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8)
        medico = Medico.objects.get(user__username=medico_user)
        
        data_1 = request.POST['data1']
        ano_1 = int(data_1[0:4])
        mes_1 = int(data_1[5:7])
        dia_1 = int(data_1[8:])
        horario_1 = request.POST['horario1']
        if horario_1 == 'Escolha o horário':
            return lesoes_render_error(request, 'Você não escolheu seu horário 1!', medico, data_1, horario_1)
        hora_1 = int(horario_1[0:2])
        minuto_1 = int(horario_1[2:])

        data_2 = request.POST['data2']
        ano_2 = int(data_2[0:4])
        mes_2 = int(data_2[5:7])
        dia_2 = int(data_2[8:])
        horario_2 = request.POST['horario2']
        if horario_2 == 'Escolha o horário':
            return lesoes_render_error(request, 'Você não escolheu seu horário 2!', medico, data_1, horario_1, data_2, horario_2)
        hora_2 = int(horario_2[0:2])
        minuto_2 = int(horario_2[2:])

        data_3 = request.POST['data3']
        ano_3 = int(data_3[0:4])
        mes_3 = int(data_3[5:7])
        dia_3 = int(data_3[8:])
        horario_3 = request.POST['horario3']
        if horario_3 == 'Escolha o horário':
            return lesoes_render_error(request, 'Você não escolheu seu horário 3!', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3)
        hora_3 = int(horario_3[0:2])
        minuto_3 = int(horario_3[2:])

        data_4 = request.POST['data4']
        ano_4 = int(data_4[0:4])
        mes_4 = int(data_4[5:7])
        dia_4 = int(data_4[8:])
        horario_4 = request.POST['horario4']
        if horario_4 == 'Escolha o horário':
            return lesoes_render_error(request, 'Você não escolheu seu horário 4!', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4)
        hora_4 = int(horario_4[0:2])
        minuto_4 = int(horario_4[2:])

        data_5 = request.POST['data5']
        ano_5 = int(data_5[0:4])
        mes_5 = int(data_5[5:7])
        dia_5 = int(data_5[8:])
        horario_5 = request.POST['horario5']
        if horario_5 == 'Escolha o horário':
            return lesoes_render_error(request, 'Você não escolheu seu horário 5!', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5)        
        hora_5 = int(horario_5[0:2])
        minuto_5 = int(horario_5[2:])

        data_6 = request.POST['data6']
        ano_6 = int(data_6[0:4])
        mes_6 = int(data_6[5:7])
        dia_6 = int(data_6[8:])
        horario_6 = request.POST['horario6']
        if horario_6 == 'Escolha o horário':
            return lesoes_render_error(request, 'Você não escolheu seu horário 6!', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6)
        hora_6 = int(horario_6[0:2])
        minuto_6 = int(horario_6[2:])

        data_7 = request.POST['data7']
        ano_7 = int(data_7[0:4])
        mes_7 = int(data_7[5:7])
        dia_7 = int(data_7[8:])
        horario_7 = request.POST['horario7']
        if horario_7 == 'Escolha o horário':
            return lesoes_render_error(request, 'Você não escolheu seu horário 7!', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7)        
        hora_7 = int(horario_7[0:2])
        minuto_7 = int(horario_7[2:])

        data_8 = request.POST['data8']
        ano_8 = int(data_8[0:4])
        mes_8 = int(data_8[5:7])
        dia_8 = int(data_8[8:])
        horario_8 = request.POST['horario8']
        if horario_8 == 'Escolha o horário':
            return lesoes_render_error(request, 'Você não escolheu seu horário 8!', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8)       
        hora_8 = int(horario_8[0:2])
        minuto_8 = int(horario_8[2:])

        try:
            nova_data_1 = Data.objects.create(ano=ano_1, mes=mes_1, dia=dia_1, hora=hora_1, minuto=minuto_1)
            nova_data_1.clean()
            nova_data_1.save()
        except ValidationError as e:
            error_messages = 'Sessão 1: ' + ', '.join(e.messages)
            return lesoes_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8)

        try:
            nova_data_2 = Data.objects.create(ano=ano_2, mes=mes_2, dia=dia_2, hora=hora_2, minuto=minuto_2)
            nova_data_2.clean()
            nova_data_2.save()
        except ValidationError as e:
            error_messages = 'Sessão 2: ' + ', '.join(e.messages)
            return lesoes_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8)

        try:
            nova_data_3 = Data.objects.create(ano=ano_3, mes=mes_3, dia=dia_3, hora=hora_3, minuto=minuto_3)
            nova_data_3.clean()
            nova_data_3.save()
        except ValidationError as e:
            error_messages = 'Sessão 3: ' + ', '.join(e.messages)
            return lesoes_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8)

        try:
            nova_data_4 = Data.objects.create(ano=ano_4, mes=mes_4, dia=dia_4, hora=hora_4, minuto=minuto_4)
            nova_data_4.clean()
            nova_data_4.save()
        except ValidationError as e:
            error_messages = 'Sessão 4: ' + ', '.join(e.messages)
            return lesoes_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8)

        try:
            nova_data_5 = Data.objects.create(ano=ano_5, mes=mes_5, dia=dia_5, hora=hora_5, minuto=minuto_5)
            nova_data_5.clean()
            nova_data_5.save()
        except ValidationError as e:
            error_messages = 'Sessão 5: ' + ', '.join(e.messages)
            return lesoes_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8)

        try:
            nova_data_6 = Data.objects.create(ano=ano_6, mes=mes_6, dia=dia_6, hora=hora_6, minuto=minuto_6)
            nova_data_6.clean()
            nova_data_6.save()
        except ValidationError as e:
            error_messages = 'Sessão 6: ' + ', '.join(e.messages)
            return lesoes_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8)

        try:
            nova_data_7 = Data.objects.create(ano=ano_7, mes=mes_7, dia=dia_7, hora=hora_7, minuto=minuto_7)
            nova_data_7.clean()
            nova_data_7.save()
        except ValidationError as e:
            error_messages = 'Sessão 7: ' + ', '.join(e.messages)
            return lesoes_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8)

        try:
            nova_data_8 = Data.objects.create(ano=ano_8, mes=mes_8, dia=dia_8, hora=hora_8, minuto=minuto_8)
            nova_data_8.clean()
            nova_data_8.save()
        except ValidationError as e:
            error_messages = 'Sessão 8: ' + ', '.join(e.messages)
            return lesoes_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8)
        
        if check_future(nova_data_1, nova_data_2) not in range(10,21):      
            return lesoes_render_error(request, 'A diferença entre as sessões precisa ser entre 10 a 21 dias. Cheque a diferença entre as sessões 1 e 2.', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8)
        elif check_future(nova_data_2, nova_data_3) not in range(10,21):
            return lesoes_render_error(request, 'A diferença entre as sessões precisa ser entre 10 a 21 dias. Cheque a diferença entre as sessões 2 e 3.', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8)    
        elif check_future(nova_data_3, nova_data_4) not in range(10,21):
            return lesoes_render_error(request, 'A diferença entre as sessões precisa ser entre 10 a 21 dias. Cheque a diferença entre as sessões 3 e 4.', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8)
        elif check_future(nova_data_4, nova_data_5) not in range(10,21):
            return lesoes_render_error(request, 'A diferença entre as sessões precisa ser entre 10 a 21 dias. Cheque a diferença entre as sessões 4 e 5.', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8)
        elif check_future(nova_data_5, nova_data_6) not in range(10,21):
            return lesoes_render_error(request, 'A diferença entre as sessões precisa ser entre 10 a 21 dias. Cheque a diferença entre as sessões 5 e 6.', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8)
        elif check_future(nova_data_6, nova_data_7) not in range(10,21):
            return lesoes_render_error(request, 'A diferença entre as sessões precisa ser entre 10 a 21 dias. Cheque a diferença entre as sessões 6 e 7.', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8)
        elif check_future(nova_data_7, nova_data_8) not in range(10,21):
            return lesoes_render_error(request, 'A diferença entre as sessões precisa ser entre 10 a 21 dias. Cheque a diferença entre as sessões 7 e 8.', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8)

        if Consulta.objects.filter(medico=medico, data__dia=dia_1, data__mes=mes_1, data__ano=ano_1, data__hora=hora_1, data__minuto=minuto_1).exists():
            error_messages = f'Data 1 inválida: {nova_data_1}, esse médico já tem compromisso para esse horário.'
            return lesoes_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8)
        
        if Consulta.objects.filter(medico=medico, data__dia=dia_2, data__mes=mes_2, data__ano=ano_2, data__hora=hora_2, data__minuto=minuto_2).exists():
            error_messages = f'Data 2 inválida: {nova_data_2}, esse médico já tem compromisso para esse horário.'
            return lesoes_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8)
        
        if Consulta.objects.filter(medico=medico, data__dia=dia_3, data__mes=mes_3, data__ano=ano_3, data__hora=hora_3, data__minuto=minuto_3).exists():
            error_messages = f'Data 3 inválida: {nova_data_3}, esse médico já tem compromisso para esse horário.'
            return lesoes_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8)
        
        if Consulta.objects.filter(medico=medico, data__dia=dia_4, data__mes=mes_4, data__ano=ano_4, data__hora=hora_4, data__minuto=minuto_4).exists():
            error_messages = f'Data 4 inválida: {nova_data_4}, esse médico já tem compromisso para esse horário.'
            return lesoes_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8)
        
        if Consulta.objects.filter(medico=medico, data__dia=dia_5, data__mes=mes_5, data__ano=ano_5, data__hora=hora_5, data__minuto=minuto_5).exists():
            error_messages = f'Data 5 inválida: {nova_data_5}, esse médico já tem compromisso para esse horário.'
            return lesoes_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8)
        
        if Consulta.objects.filter(medico=medico, data__dia=dia_6, data__mes=mes_6, data__ano=ano_6, data__hora=hora_6, data__minuto=minuto_6).exists():
            error_messages = f'Data 6 inválida: {nova_data_6}, esse médico já tem compromisso para esse horário.'
            return lesoes_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8)
        
        if Consulta.objects.filter(medico=medico, data__dia=dia_7, data__mes=mes_7, data__ano=ano_7, data__hora=hora_7, data__minuto=minuto_7).exists():
            error_messages = f'Data 7 inválida: {nova_data_7}, esse médico já tem compromisso para esse horário.'
            return lesoes_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8)
        
        if Consulta.objects.filter(medico=medico, data__dia=dia_8, data__mes=mes_8, data__ano=ano_8, data__hora=hora_8, data__minuto=minuto_8).exists():
            error_messages = f'Data 8 inválida: {nova_data_8}, esse médico já tem compromisso para esse horário.'
            return lesoes_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8)
        
        try:
            consulta = Consulta.objects.create(paciente=paciente, servico='lesoes', medico=medico, data=nova_data_1)
            consulta.save()
            consulta2 = Consulta.objects.create(paciente=paciente, servico='lesoes', medico=medico, data=nova_data_2)
            consulta2.save()
            consulta3 = Consulta.objects.create(paciente=paciente, servico='lesoes', medico=medico, data=nova_data_3)
            consulta3.save()
            consulta4 = Consulta.objects.create(paciente=paciente, servico='lesoes', medico=medico, data=nova_data_4)
            consulta4.save()
            consulta5 = Consulta.objects.create(paciente=paciente, servico='lesoes', medico=medico, data=nova_data_5)
            consulta5.save()
            consulta6 = Consulta.objects.create(paciente=paciente, servico='lesoes', medico=medico, data=nova_data_6)
            consulta6.save()
            consulta7 = Consulta.objects.create(paciente=paciente, servico='lesoes', medico=medico, data=nova_data_7)
            consulta7.save()
            consulta8 = Consulta.objects.create(paciente=paciente, servico='lesoes', medico=medico, data=nova_data_8)
            consulta8.save()
        except:
            error_messages = 'Algo deu errado :/ Tente novamente'
            return lesoes_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8)
        
        messages.success(request, f'Tratamento de Lesões: {paciente} com {medico.nome_completo} - Marcado com sucesso')
        return redirect('dashboard')
    else:
        context = {
                'horarios': time_choices,
                'medicos': Medico.objects.all().filter(lesoes=True),
            }
        return render(request, 'consultas/lesoes.html', context)

def pos_cirurgia(request):
    if request.method == 'POST':
        paciente = request.user.paciente
        
        medico_user = request.POST['medico']
        if medico_user == 'Escolha seu médico':
            return pos_cirurgia_render_error(request, 'Você não escolheu seu médico!', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10)
        medico = Medico.objects.get(user__username=medico_user)
        
        data_1 = request.POST['data1']
        ano_1 = int(data_1[0:4])
        mes_1 = int(data_1[5:7])
        dia_1 = int(data_1[8:])
        horario_1 = request.POST['horario1']
        if horario_1 == 'Escolha o horário':
            return pos_cirurgia_render_error(request, 'Você não escolheu seu horário 1!', medico, data_1, horario_1)
        hora_1 = int(horario_1[0:2])
        minuto_1 = int(horario_1[2:])

        data_2 = request.POST['data2']
        ano_2 = int(data_2[0:4])
        mes_2 = int(data_2[5:7])
        dia_2 = int(data_2[8:])
        horario_2 = request.POST['horario2']
        if horario_2 == 'Escolha o horário':
            return pos_cirurgia_render_error(request, 'Você não escolheu seu horário 2!', medico, data_1, horario_1, data_2, horario_2)
        hora_2 = int(horario_2[0:2])
        minuto_2 = int(horario_2[2:])

        data_3 = request.POST['data3']
        ano_3 = int(data_3[0:4])
        mes_3 = int(data_3[5:7])
        dia_3 = int(data_3[8:])
        horario_3 = request.POST['horario3']
        if horario_3 == 'Escolha o horário':
            return pos_cirurgia_render_error(request, 'Você não escolheu seu horário 3!', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3)
        hora_3 = int(horario_3[0:2])
        minuto_3 = int(horario_3[2:])

        data_4 = request.POST['data4']
        ano_4 = int(data_4[0:4])
        mes_4 = int(data_4[5:7])
        dia_4 = int(data_4[8:])
        horario_4 = request.POST['horario4']
        if horario_4 == 'Escolha o horário':
            return pos_cirurgia_render_error(request, 'Você não escolheu seu horário 4!', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4)
        hora_4 = int(horario_4[0:2])
        minuto_4 = int(horario_4[2:])

        data_5 = request.POST['data5']
        ano_5 = int(data_5[0:4])
        mes_5 = int(data_5[5:7])
        dia_5 = int(data_5[8:])
        horario_5 = request.POST['horario5']
        if horario_5 == 'Escolha o horário':
            return pos_cirurgia_render_error(request, 'Você não escolheu seu horário 5!', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5)        
        hora_5 = int(horario_5[0:2])
        minuto_5 = int(horario_5[2:])

        data_6 = request.POST['data6']
        ano_6 = int(data_6[0:4])
        mes_6 = int(data_6[5:7])
        dia_6 = int(data_6[8:])
        horario_6 = request.POST['horario6']
        if horario_6 == 'Escolha o horário':
            return pos_cirurgia_render_error(request, 'Você não escolheu seu horário 6!', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6)
        hora_6 = int(horario_6[0:2])
        minuto_6 = int(horario_6[2:])

        data_7 = request.POST['data7']
        ano_7 = int(data_7[0:4])
        mes_7 = int(data_7[5:7])
        dia_7 = int(data_7[8:])
        horario_7 = request.POST['horario7']
        if horario_7 == 'Escolha o horário':
            return pos_cirurgia_render_error(request, 'Você não escolheu seu horário 7!', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7)        
        hora_7 = int(horario_7[0:2])
        minuto_7 = int(horario_7[2:])

        data_8 = request.POST['data8']
        ano_8 = int(data_8[0:4])
        mes_8 = int(data_8[5:7])
        dia_8 = int(data_8[8:])
        horario_8 = request.POST['horario8']
        if horario_8 == 'Escolha o horário':
            return pos_cirurgia_render_error(request, 'Você não escolheu seu horário 8!', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8)       
        hora_8 = int(horario_8[0:2])
        minuto_8 = int(horario_8[2:])

        data_9 = request.POST['data9']
        ano_9 = int(data_9[0:4])
        mes_9 = int(data_9[5:7])
        dia_9 = int(data_9[8:])
        horario_9 = request.POST['horario9']
        if horario_9 == 'Escolha o horário':
            return pos_cirurgia_render_error(request, 'Você não escolheu seu horário 9!', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9)
        hora_9 = int(horario_9[0:2])
        minuto_9 = int(horario_9[2:])

        data_10 = request.POST['data10']
        ano_10 = int(data_10[0:4])
        mes_10 = int(data_10[5:7])
        dia_10 = int(data_10[8:])
        horario_10 = request.POST['horario10']
        if horario_10 == 'Escolha o horário':
            return pos_cirurgia_render_error(request, 'Você não escolheu seu horário 10!', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10)       
        hora_10 = int(horario_10[0:2])
        minuto_10 = int(horario_10[2:])
 
        try:
            nova_data_1 = Data.objects.create(ano=ano_1, mes=mes_1, dia=dia_1, hora=hora_1, minuto=minuto_1)
            nova_data_1.clean()
            nova_data_1.save()
        except ValidationError as e:
            error_messages = 'Sessão 1: ' + ', '.join(e.messages)
            return pos_cirurgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10)

        try:
            nova_data_2 = Data.objects.create(ano=ano_2, mes=mes_2, dia=dia_2, hora=hora_2, minuto=minuto_2)
            nova_data_2.clean()
            nova_data_2.save()
        except ValidationError as e:
            error_messages = 'Sessão 2: ' + ', '.join(e.messages)
            return pos_cirurgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10)

        try:
            nova_data_3 = Data.objects.create(ano=ano_3, mes=mes_3, dia=dia_3, hora=hora_3, minuto=minuto_3)
            nova_data_3.clean()
            nova_data_3.save()
        except ValidationError as e:
            error_messages = 'Sessão 3: ' + ', '.join(e.messages)
            return pos_cirurgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10)

        try:
            nova_data_4 = Data.objects.create(ano=ano_4, mes=mes_4, dia=dia_4, hora=hora_4, minuto=minuto_4)
            nova_data_4.clean()
            nova_data_4.save()
        except ValidationError as e:
            error_messages = 'Sessão 4: ' + ', '.join(e.messages)
            return pos_cirurgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10)

        try:
            nova_data_5 = Data.objects.create(ano=ano_5, mes=mes_5, dia=dia_5, hora=hora_5, minuto=minuto_5)
            nova_data_5.clean()
            nova_data_5.save()
        except ValidationError as e:
            error_messages = 'Sessão 5: ' + ', '.join(e.messages)
            return pos_cirurgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10)

        try:
            nova_data_6 = Data.objects.create(ano=ano_6, mes=mes_6, dia=dia_6, hora=hora_6, minuto=minuto_6)
            nova_data_6.clean()
            nova_data_6.save()
        except ValidationError as e:
            error_messages = 'Sessão 6: ' + ', '.join(e.messages)
            return pos_cirurgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10)

        try:
            nova_data_7 = Data.objects.create(ano=ano_7, mes=mes_7, dia=dia_7, hora=hora_7, minuto=minuto_7)
            nova_data_7.clean()
            nova_data_7.save()
        except ValidationError as e:
            error_messages = 'Sessão 7: ' + ', '.join(e.messages)
            return pos_cirurgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10)

        try:
            nova_data_8 = Data.objects.create(ano=ano_8, mes=mes_8, dia=dia_8, hora=hora_8, minuto=minuto_8)
            nova_data_8.clean()
            nova_data_8.save()
        except ValidationError as e:
            error_messages = 'Sessão 8: ' + ', '.join(e.messages)
            return pos_cirurgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10)

        try:
            nova_data_9 = Data.objects.create(ano=ano_9, mes=mes_9, dia=dia_9, hora=hora_9, minuto=minuto_9)
            nova_data_9.clean()
            nova_data_9.save()
        except ValidationError as e:
            error_messages = 'Sessão 9: ' + ', '.join(e.messages)
            return pos_cirurgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10)
        
        try:
            nova_data_10 = Data.objects.create(ano=ano_10, mes=mes_10, dia=dia_10, hora=hora_10, minuto=minuto_10)
            nova_data_10.clean()
            nova_data_10.save()
        except ValidationError as e:
            error_messages = 'Sessão 10: ' + ', '.join(e.messages)
            return pos_cirurgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10)
        
        if check_future(nova_data_1, nova_data_2) not in range(7,14):      
            return pos_cirurgia_render_error(request, 'A diferença entre as sessões precisa ser entre 7 a 14 dias. Cheque a diferença entre as sessões 1 e 2.', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10)
        elif check_future(nova_data_2, nova_data_3) not in range(7,14):
            return pos_cirurgia_render_error(request, 'A diferença entre as sessões precisa ser entre 7 a 14 dias. Cheque a diferença entre as sessões 2 e 3.', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10)    
        elif check_future(nova_data_3, nova_data_4) not in range(7,14):
            return pos_cirurgia_render_error(request, 'A diferença entre as sessões precisa ser entre 7 a 14 dias. Cheque a diferença entre as sessões 3 e 4.', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10)
        elif check_future(nova_data_4, nova_data_5) not in range(7,14):
            return pos_cirurgia_render_error(request, 'A diferença entre as sessões precisa ser entre 7 a 14 dias. Cheque a diferença entre as sessões 4 e 5.', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10)
        elif check_future(nova_data_5, nova_data_6) not in range(7,14):
            return pos_cirurgia_render_error(request, 'A diferença entre as sessões precisa ser entre 7 a 14 dias. Cheque a diferença entre as sessões 5 e 6.', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10)
        elif check_future(nova_data_6, nova_data_7) not in range(7,14):
            return pos_cirurgia_render_error(request, 'A diferença entre as sessões precisa ser entre 7 a 14 dias. Cheque a diferença entre as sessões 6 e 7.', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10)
        elif check_future(nova_data_7, nova_data_8) not in range(7,14):
            return pos_cirurgia_render_error(request, 'A diferença entre as sessões precisa ser entre 7 a 14 dias. Cheque a diferença entre as sessões 7 e 8.', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10)
        elif check_future(nova_data_8, nova_data_9) not in range(7,14):
            return pos_cirurgia_render_error(request, 'A diferença entre as sessões precisa ser entre 7 a 14 dias. Cheque a diferença entre as sessões 8 e 9.', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10)
        elif check_future(nova_data_9, nova_data_10) not in range(7,14):
            return pos_cirurgia_render_error(request, 'A diferença entre as sessões precisa ser entre 7 a 14 dias. Cheque a diferença entre as sessões 9 e 10.', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10)

        if Consulta.objects.filter(medico=medico, data__dia=dia_1, data__mes=mes_1, data__ano=ano_1, data__hora=hora_1, data__minuto=minuto_1).exists():
            error_messages = f'Data 1 inválida: {nova_data_1}, esse médico já tem compromisso para esse horário.'
            return pos_cirurgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10)
        
        if Consulta.objects.filter(medico=medico, data__dia=dia_2, data__mes=mes_2, data__ano=ano_2, data__hora=hora_2, data__minuto=minuto_2).exists():
            error_messages = f'Data 2 inválida: {nova_data_2}, esse médico já tem compromisso para esse horário.'
            return pos_cirurgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10)
        
        if Consulta.objects.filter(medico=medico, data__dia=dia_3, data__mes=mes_3, data__ano=ano_3, data__hora=hora_3, data__minuto=minuto_3).exists():
            error_messages = f'Data 3 inválida: {nova_data_3}, esse médico já tem compromisso para esse horário.'
            return pos_cirurgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10)
        
        if Consulta.objects.filter(medico=medico, data__dia=dia_4, data__mes=mes_4, data__ano=ano_4, data__hora=hora_4, data__minuto=minuto_4).exists():
            error_messages = f'Data 4 inválida: {nova_data_4}, esse médico já tem compromisso para esse horário.'
            return pos_cirurgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10)
        
        if Consulta.objects.filter(medico=medico, data__dia=dia_5, data__mes=mes_5, data__ano=ano_5, data__hora=hora_5, data__minuto=minuto_5).exists():
            error_messages = f'Data 5 inválida: {nova_data_5}, esse médico já tem compromisso para esse horário.'
            return pos_cirurgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10)
        
        if Consulta.objects.filter(medico=medico, data__dia=dia_6, data__mes=mes_6, data__ano=ano_6, data__hora=hora_6, data__minuto=minuto_6).exists():
            error_messages = f'Data 6 inválida: {nova_data_6}, esse médico já tem compromisso para esse horário.'
            return pos_cirurgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10)
        
        if Consulta.objects.filter(medico=medico, data__dia=dia_7, data__mes=mes_7, data__ano=ano_7, data__hora=hora_7, data__minuto=minuto_7).exists():
            error_messages = f'Data 7 inválida: {nova_data_7}, esse médico já tem compromisso para esse horário.'
            return pos_cirurgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10)
        
        if Consulta.objects.filter(medico=medico, data__dia=dia_8, data__mes=mes_8, data__ano=ano_8, data__hora=hora_8, data__minuto=minuto_8).exists():
            error_messages = f'Data 8 inválida: {nova_data_8}, esse médico já tem compromisso para esse horário.'
            return pos_cirurgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10)
        
        if Consulta.objects.filter(medico=medico, data__dia=dia_9, data__mes=mes_9, data__ano=ano_9, data__hora=hora_9, data__minuto=minuto_9).exists():
            error_messages = f'Data 9 inválida: {nova_data_9}, esse médico já tem compromisso para esse horário.'
            return pos_cirurgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10)
        
        if Consulta.objects.filter(medico=medico, data__dia=dia_10, data__mes=mes_10, data__ano=ano_10, data__hora=hora_10, data__minuto=minuto_10).exists():
            error_messages = f'Data 10 inválida: {nova_data_10}, esse médico já tem compromisso para esse horário.'
            return pos_cirurgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10)
        
        try:
            consulta = Consulta.objects.create(paciente=paciente, servico='pos_cirurgia', medico=medico, data=nova_data_1)
            consulta.save()
            consulta2 = Consulta.objects.create(paciente=paciente, servico='pos_cirurgia', medico=medico, data=nova_data_2)
            consulta2.save()
            consulta3 = Consulta.objects.create(paciente=paciente, servico='pos_cirurgia', medico=medico, data=nova_data_3)
            consulta3.save()
            consulta4 = Consulta.objects.create(paciente=paciente, servico='pos_cirurgia', medico=medico, data=nova_data_4)
            consulta4.save()
            consulta5 = Consulta.objects.create(paciente=paciente, servico='pos_cirurgia', medico=medico, data=nova_data_5)
            consulta5.save()
            consulta6 = Consulta.objects.create(paciente=paciente, servico='pos_cirurgia', medico=medico, data=nova_data_6)
            consulta6.save()
            consulta7 = Consulta.objects.create(paciente=paciente, servico='pos_cirurgia', medico=medico, data=nova_data_7)
            consulta7.save()
            consulta8 = Consulta.objects.create(paciente=paciente, servico='pos_cirurgia', medico=medico, data=nova_data_8)
            consulta8.save()
            consulta9 = Consulta.objects.create(paciente=paciente, servico='pos_cirurgia', medico=medico, data=nova_data_9)
            consulta9.save()
            consulta10 = Consulta.objects.create(paciente=paciente, servico='pos_cirurgia', medico=medico, data=nova_data_10)
            consulta10.save()
        except:
            error_messages = 'Algo deu errado :/ Tente novamente'
            return pos_cirurgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10)
        
        messages.success(request, f'Tratamento de Pós-Cirurgia: {paciente} com {medico.nome_completo} - Marcado com sucesso')
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
            return nevralgia_render_error(request, 'Você não escolheu seu médico!', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        medico = Medico.objects.get(user__username=medico_user)
        
        data_1 = request.POST['data1']
        ano_1 = int(data_1[0:4])
        mes_1 = int(data_1[5:7])
        dia_1 = int(data_1[8:])
        horario_1 = request.POST['horario1']
        if horario_1 == 'Escolha o horário':
            return nevralgia_render_error(request, 'Você não escolheu seu horário 1!', medico, data_1, horario_1)
        hora_1_1 = int(horario_1[0:2])
        minuto_1_1 = int(horario_1[2:])

        if minuto_1_1 == 30:
            minuto_1_2 = 0
            hora_1_2 = hora_1_1 + 1
        else:
            minuto_1_2 = 30
            hora_1_2 = hora_1_1

        data_2 = request.POST['data2']
        ano_2 = int(data_2[0:4])
        mes_2 = int(data_2[5:7])
        dia_2 = int(data_2[8:])
        horario_2 = request.POST['horario2']
        if horario_2 == 'Escolha o horário':
            return nevralgia_render_error(request, 'Você não escolheu seu horário 2!', medico, data_1, horario_1, data_2, horario_2)
        hora_2_1 = int(horario_2[0:2])
        minuto_2_1 = int(horario_2[2:])

        if minuto_2_1 == 30:
            minuto_2_2 = 0
            hora_2_2 = hora_2_1 + 1
        else:
            minuto_2_2 = 30
            hora_2_2 = hora_2_1

        data_3 = request.POST['data3']
        ano_3 = int(data_3[0:4])
        mes_3 = int(data_3[5:7])
        dia_3 = int(data_3[8:])
        horario_3 = request.POST['horario3']
        if horario_3 == 'Escolha o horário':
            return nevralgia_render_error(request, 'Você não escolheu seu horário 3!', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3)
        hora_3_1 = int(horario_3[0:2])
        minuto_3_1 = int(horario_3[2:])

        if minuto_3_1 == 30:
            minuto_3_2 = 0
            hora_3_2 = hora_3_1 + 1
        else:
            minuto_3_2 = 30
            hora_3_2 = hora_3_1

        data_4 = request.POST['data4']
        ano_4 = int(data_4[0:4])
        mes_4 = int(data_4[5:7])
        dia_4 = int(data_4[8:])
        horario_4 = request.POST['horario4']
        if horario_4 == 'Escolha o horário':
            return nevralgia_render_error(request, 'Você não escolheu seu horário 4!', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4)
        hora_4_1 = int(horario_4[0:2])
        minuto_4_1 = int(horario_4[2:])

        if minuto_4_1 == 30:
            minuto_4_2 = 0
            hora_4_2 = hora_4_1 + 1
        else:
            minuto_4_2 = 30
            hora_4_2 = hora_4_1

        data_5 = request.POST['data5']
        ano_5 = int(data_5[0:4])
        mes_5 = int(data_5[5:7])
        dia_5 = int(data_5[8:])
        horario_5 = request.POST['horario5']
        if horario_5 == 'Escolha o horário':
            return nevralgia_render_error(request, 'Você não escolheu seu horário 5!', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5)        
        hora_5_1 = int(horario_5[0:2])
        minuto_5_1 = int(horario_5[2:])

        if minuto_5_1 == 30:
            minuto_5_2 = 0
            hora_5_2 = hora_5_1 + 1
        else:
            minuto_5_2 = 30
            hora_5_2 = hora_5_1

        data_6 = request.POST['data6']
        ano_6 = int(data_6[0:4])
        mes_6 = int(data_6[5:7])
        dia_6 = int(data_6[8:])
        horario_6 = request.POST['horario6']
        if horario_6 == 'Escolha o horário':
            return nevralgia_render_error(request, 'Você não escolheu seu horário 6!', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6)
        hora_6_1 = int(horario_6[0:2])
        minuto_6_1 = int(horario_6[2:])

        if minuto_6_1 == 30:
            minuto_6_2 = 0
            hora_6_2 = hora_6_1 + 1
        else:
            minuto_6_2 = 30
            hora_6_2 = hora_6_1

        data_7 = request.POST['data7']
        ano_7 = int(data_7[0:4])
        mes_7 = int(data_7[5:7])
        dia_7 = int(data_7[8:])
        horario_7 = request.POST['horario7']
        if horario_7 == 'Escolha o horário':
            return nevralgia_render_error(request, 'Você não escolheu seu horário 7!', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7)        
        hora_7_1 = int(horario_7[0:2])
        minuto_7_1 = int(horario_7[2:])

        if minuto_7_1 == 30:
            minuto_7_2 = 0
            hora_7_2 = hora_7_1 + 1
        else:
            minuto_7_2 = 30
            hora_7_2 = hora_7_1

        data_8 = request.POST['data8']
        ano_8 = int(data_8[0:4])
        mes_8 = int(data_8[5:7])
        dia_8 = int(data_8[8:])
        horario_8 = request.POST['horario8']
        if horario_8 == 'Escolha o horário':
            return nevralgia_render_error(request, 'Você não escolheu seu horário 8!', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8)       
        hora_8_1 = int(horario_8[0:2])
        minuto_8_1 = int(horario_8[2:])

        if minuto_8_1 == 30:
            minuto_8_2 = 0
            hora_8_2 = hora_8_1 + 1
        else:
            minuto_8_2 = 30
            hora_8_2 = hora_8_1

        data_9 = request.POST['data9']
        ano_9 = int(data_9[0:4])
        mes_9 = int(data_9[5:7])
        dia_9 = int(data_9[8:])
        horario_9 = request.POST['horario9']
        if horario_9 == 'Escolha o horário':
            return nevralgia_render_error(request, 'Você não escolheu seu horário 9!', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9)
        hora_9_1 = int(horario_9[0:2])
        minuto_9_1 = int(horario_9[2:])

        if minuto_9_1 == 30:
            minuto_9_2 = 0
            hora_9_2 = hora_9_1 + 1
        else:
            minuto_9_2 = 30
            hora_9_2 = hora_9_1

        data_10 = request.POST['data10']
        ano_10 = int(data_10[0:4])
        mes_10 = int(data_10[5:7])
        dia_10 = int(data_10[8:])
        horario_10 = request.POST['horario10']
        if horario_10 == 'Escolha o horário':
            return nevralgia_render_error(request, 'Você não escolheu seu horário 10!', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10)       
        hora_10_1 = int(horario_10[0:2])
        minuto_10_1 = int(horario_10[2:])

        if minuto_10_1 == 30:
            minuto_10_2 = 0
            hora_10_2 = hora_10_1 + 1
        else:
            minuto_10_2 = 30
            hora_10_2 = hora_10_1

        data_11 = request.POST['data11']
        ano_11 = int(data_11[0:4])
        mes_11 = int(data_11[5:7])
        dia_11 = int(data_11[8:])
        horario_11 = request.POST['horario11']
        if horario_11 == 'Escolha o horário':
            return nevralgia_render_error(request, 'Você não escolheu seu horário 11!', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11)       
        hora_11_1 = int(horario_11[0:2])
        minuto_11_1 = int(horario_11[2:])

        if minuto_11_1 == 30:
            minuto_11_2 = 0
            hora_11_2 = hora_11_1 + 1
        else:
            minuto_11_2 = 30
            hora_11_2 = hora_11_1

        data_12 = request.POST['data12']
        ano_12 = int(data_12[0:4])
        mes_12 = int(data_12[5:7])
        dia_12 = int(data_12[8:])
        horario_12 = request.POST['horario12']
        if horario_12 == 'Escolha o horário':
            return nevralgia_render_error(request, 'Você não escolheu seu horário 12!', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12)       
        hora_12_1 = int(horario_12[0:2])
        minuto_12_1 = int(horario_12[2:])

        if minuto_12_1 == 30:
            minuto_12_2 = 0
            hora_12_2 = hora_12_1 + 1
        else:
            minuto_12_2 = 30
            hora_12_2 = hora_12_1

        data_13 = request.POST['data13']
        ano_13 = int(data_13[0:4])
        mes_13 = int(data_13[5:7])
        dia_13 = int(data_13[8:])
        horario_13 = request.POST['horario13']
        if horario_13 == 'Escolha o horário':
            return nevralgia_render_error(request, 'Você não escolheu seu horário 13!', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13)       
        hora_13_1 = int(horario_13[0:2])
        minuto_13_1 = int(horario_13[2:])

        if minuto_13_1 == 30:
            minuto_13_2 = 0
            hora_13_2 = hora_13_1 + 1
        else:
            minuto_13_2 = 30
            hora_13_2 = hora_13_1

        data_14 = request.POST['data14']
        ano_14 = int(data_14[0:4])
        mes_14 = int(data_14[5:7])
        dia_14 = int(data_14[8:])
        horario_14 = request.POST['horario14']
        if horario_14 == 'Escolha o horário':
            return nevralgia_render_error(request, 'Você não escolheu seu horário 14!', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14)       
        hora_14_1 = int(horario_14[0:2])
        minuto_14_1 = int(horario_14[2:])

        if minuto_14_1 == 30:
            minuto_14_2 = 0
            hora_14_2 = hora_14_1 + 1
        else:
            minuto_14_2 = 30
            hora_14_2 = hora_14_1

        data_15 = request.POST['data15']
        ano_15 = int(data_15[0:4])
        mes_15 = int(data_15[5:7])
        dia_15 = int(data_15[8:])
        horario_15 = request.POST['horario15']
        if horario_15 == 'Escolha o horário':
            return nevralgia_render_error(request, 'Você não escolheu seu horário 15!', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)       
        hora_15_1 = int(horario_15[0:2])
        minuto_15_1 = int(horario_15[2:])

        if minuto_15_1 == 30:
            minuto_15_2 = 0
            hora_15_2 = hora_15_1 + 1
        else:
            minuto_15_2 = 30
            hora_15_2 = hora_15_1
 
        try:
            nova_data_1_1 = Data.objects.create(ano=ano_1, mes=mes_1, dia=dia_1, hora=hora_1_1, minuto=minuto_1_1)
            nova_data_1_1.clean()
            nova_data_1_1.save()
        except ValidationError as e:
            error_messages = 'Sessão 1: ' + ', '.join(e.messages)
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        
        try:
            nova_data_1_2 = Data.objects.create(ano=ano_1, mes=mes_1, dia=dia_1, hora=hora_1_2, minuto=minuto_1_2)
            nova_data_1_2.clean()
            nova_data_1_2.save()
        except ValidationError as e:
            error_messages = 'Sessão 1: ' + ', '.join(e.messages)
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)

        try:
            nova_data_2_1 = Data.objects.create(ano=ano_2, mes=mes_2, dia=dia_2, hora=hora_2_1, minuto=minuto_2_1)
            nova_data_2_1.clean()
            nova_data_2_1.save()
        except ValidationError as e:
            error_messages = 'Sessão 2: ' + ', '.join(e.messages)
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        
        try:
            nova_data_2_2 = Data.objects.create(ano=ano_2, mes=mes_2, dia=dia_2, hora=hora_2_2, minuto=minuto_2_2)
            nova_data_2_2.clean()
            nova_data_2_2.save()
        except ValidationError as e:
            error_messages = 'Sessão 2: ' + ', '.join(e.messages)
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        
        try:
            nova_data_3_1 = Data.objects.create(ano=ano_3, mes=mes_3, dia=dia_3, hora=hora_3_1, minuto=minuto_3_1)
            nova_data_3_1.clean()
            nova_data_3_1.save()
        except ValidationError as e:
            error_messages = 'Sessão 3: ' + ', '.join(e.messages)
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        
        try:
            nova_data_3_2 = Data.objects.create(ano=ano_3, mes=mes_3, dia=dia_3, hora=hora_3_2, minuto=minuto_3_2)
            nova_data_3_2.clean()
            nova_data_3_2.save()
        except ValidationError as e:
            error_messages = 'Sessão 3: ' + ', '.join(e.messages)
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)

        try:
            nova_data_4_1 = Data.objects.create(ano=ano_4, mes=mes_4, dia=dia_4, hora=hora_4_1, minuto=minuto_4_1)
            nova_data_4_1.clean()
            nova_data_4_1.save()
        except ValidationError as e:
            error_messages = 'Sessão 4: ' + ', '.join(e.messages)
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        
        try:
            nova_data_4_2 = Data.objects.create(ano=ano_4, mes=mes_4, dia=dia_4, hora=hora_4_2, minuto=minuto_4_2)
            nova_data_4_2.clean()
            nova_data_4_2.save()
        except ValidationError as e:
            error_messages = 'Sessão 4: ' + ', '.join(e.messages)
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)

        try:
            nova_data_5_1 = Data.objects.create(ano=ano_5, mes=mes_5, dia=dia_5, hora=hora_5_1, minuto=minuto_5_1)
            nova_data_5_1.clean()
            nova_data_5_1.save()
        except ValidationError as e:
            error_messages = 'Sessão 5: ' + ', '.join(e.messages)
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        
        try:
            nova_data_5_2 = Data.objects.create(ano=ano_5, mes=mes_5, dia=dia_5, hora=hora_5_2, minuto=minuto_5_2)
            nova_data_5_2.clean()
            nova_data_5_2.save()
        except ValidationError as e:
            error_messages = 'Sessão 5: ' + ', '.join(e.messages)
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)

        try:
            nova_data_6_1 = Data.objects.create(ano=ano_6, mes=mes_6, dia=dia_6, hora=hora_6_1, minuto=minuto_6_1)
            nova_data_6_1.clean()
            nova_data_6_1.save()
        except ValidationError as e:
            error_messages = 'Sessão 6: ' + ', '.join(e.messages)
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        
        try:
            nova_data_6_2 = Data.objects.create(ano=ano_6, mes=mes_6, dia=dia_6, hora=hora_6_2, minuto=minuto_6_2)
            nova_data_6_2.clean()
            nova_data_6_2.save()
        except ValidationError as e:
            error_messages = 'Sessão 6: ' + ', '.join(e.messages)
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)

        try:
            nova_data_7_1 = Data.objects.create(ano=ano_7, mes=mes_7, dia=dia_7, hora=hora_7_1, minuto=minuto_7_1)
            nova_data_7_1.clean()
            nova_data_7_1.save()
        except ValidationError as e:
            error_messages = 'Sessão 7: ' + ', '.join(e.messages)
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        
        try:
            nova_data_7_2 = Data.objects.create(ano=ano_7, mes=mes_7, dia=dia_7, hora=hora_7_2, minuto=minuto_7_2)
            nova_data_7_2.clean()
            nova_data_7_2.save()
        except ValidationError as e:
            error_messages = 'Sessão 7: ' + ', '.join(e.messages)
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)

        try:
            nova_data_8_1 = Data.objects.create(ano=ano_8, mes=mes_8, dia=dia_8, hora=hora_8_1, minuto=minuto_8_1)
            nova_data_8_1.clean()
            nova_data_8_1.save()
        except ValidationError as e:
            error_messages = 'Sessão 8: ' + ', '.join(e.messages)
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)

        try:
            nova_data_8_2 = Data.objects.create(ano=ano_8, mes=mes_8, dia=dia_8, hora=hora_8_2, minuto=minuto_8_2)
            nova_data_8_2.clean()
            nova_data_8_2.save()
        except ValidationError as e:
            error_messages = 'Sessão 8: ' + ', '.join(e.messages)
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)

        try:
            nova_data_9_1 = Data.objects.create(ano=ano_9, mes=mes_9, dia=dia_9, hora=hora_9_1, minuto=minuto_9_1)
            nova_data_9_1.clean()
            nova_data_9_1.save()
        except ValidationError as e:
            error_messages = 'Sessão 9: ' + ', '.join(e.messages)
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        
        try:
            nova_data_9_2 = Data.objects.create(ano=ano_9, mes=mes_9, dia=dia_9, hora=hora_9_2, minuto=minuto_9_2)
            nova_data_9_2.clean()
            nova_data_9_2.save()
        except ValidationError as e:
            error_messages = 'Sessão 9: ' + ', '.join(e.messages)
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        
        try:
            nova_data_10_1 = Data.objects.create(ano=ano_10, mes=mes_10, dia=dia_10, hora=hora_10_1, minuto=minuto_10_1)
            nova_data_10_1.clean()
            nova_data_10_1.save()
        except ValidationError as e:
            error_messages = 'Sessão 10: ' + ', '.join(e.messages)
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        
        try:
            nova_data_10_2 = Data.objects.create(ano=ano_10, mes=mes_10, dia=dia_10, hora=hora_10_2, minuto=minuto_10_2)
            nova_data_10_2.clean()
            nova_data_10_2.save()
        except ValidationError as e:
            error_messages = 'Sessão 10: ' + ', '.join(e.messages)
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        
        try:
            nova_data_11_1 = Data.objects.create(ano=ano_11, mes=mes_11, dia=dia_11, hora=hora_11_1, minuto=minuto_11_1)
            nova_data_11_1.clean()
            nova_data_11_1.save()
        except ValidationError as e:
            error_messages = 'Sessão 11: ' + ', '.join(e.messages)
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        
        try:
            nova_data_11_2 = Data.objects.create(ano=ano_11, mes=mes_11, dia=dia_11, hora=hora_11_2, minuto=minuto_11_2)
            nova_data_11_2.clean()
            nova_data_11_2.save()
        except ValidationError as e:
            error_messages = 'Sessão 11: ' + ', '.join(e.messages)
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        
        try:
            nova_data_12_1 = Data.objects.create(ano=ano_12, mes=mes_12, dia=dia_12, hora=hora_12_1, minuto=minuto_12_1)
            nova_data_12_1.clean()
            nova_data_12_1.save()
        except ValidationError as e:
            error_messages = 'Sessão 12: ' + ', '.join(e.messages)
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        
        try:
            nova_data_12_2 = Data.objects.create(ano=ano_12, mes=mes_12, dia=dia_12, hora=hora_12_2, minuto=minuto_12_2)
            nova_data_12_2.clean()
            nova_data_12_2.save()
        except ValidationError as e:
            error_messages = 'Sessão 12: ' + ', '.join(e.messages)
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        
        try:
            nova_data_13_1 = Data.objects.create(ano=ano_13, mes=mes_13, dia=dia_13, hora=hora_13_1, minuto=minuto_13_1)
            nova_data_13_1.clean()
            nova_data_13_1.save()
        except ValidationError as e:
            error_messages = 'Sessão 13: ' + ', '.join(e.messages)
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        
        try:
            nova_data_13_2 = Data.objects.create(ano=ano_13, mes=mes_13, dia=dia_13, hora=hora_13_2, minuto=minuto_13_2)
            nova_data_13_2.clean()
            nova_data_13_2.save()
        except ValidationError as e:
            error_messages = 'Sessão 13: ' + ', '.join(e.messages)
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        
        try:
            nova_data_14_1 = Data.objects.create(ano=ano_14, mes=mes_14, dia=dia_14, hora=hora_14_1, minuto=minuto_14_1)
            nova_data_14_1.clean()
            nova_data_14_1.save()
        except ValidationError as e:
            error_messages = 'Sessão 14: ' + ', '.join(e.messages)
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        
        try:
            nova_data_14_2 = Data.objects.create(ano=ano_14, mes=mes_14, dia=dia_14, hora=hora_14_2, minuto=minuto_14_2)
            nova_data_14_2.clean()
            nova_data_14_2.save()
        except ValidationError as e:
            error_messages = 'Sessão 14: ' + ', '.join(e.messages)
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        
        try:
            nova_data_15_1 = Data.objects.create(ano=ano_15, mes=mes_15, dia=dia_15, hora=hora_15_1, minuto=minuto_15_1)
            nova_data_15_1.clean()
            nova_data_15_1.save()
        except ValidationError as e:
            error_messages = 'Sessão 15: ' + ', '.join(e.messages)
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        
        try:
            nova_data_15_2 = Data.objects.create(ano=ano_15, mes=mes_15, dia=dia_15, hora=hora_15_2, minuto=minuto_15_2)
            nova_data_15_2.clean()
            nova_data_15_2.save()
        except ValidationError as e:
            error_messages = 'Sessão 15: ' + ', '.join(e.messages)
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        
        if check_future(nova_data_1_1, nova_data_2_1) not in range(8,16):      
            return nevralgia_render_error(request, 'A diferença entre as sessões precisa ser entre 8 a 16 dias. Cheque a diferença entre as sessões 1 e 2.', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        elif check_future(nova_data_2_1, nova_data_3_1) not in range(8,16):
            return nevralgia_render_error(request, 'A diferença entre as sessões precisa ser entre 8 a 16 dias. Cheque a diferença entre as sessões 2 e 3.', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)    
        elif check_future(nova_data_3_1, nova_data_4_1) not in range(8,16):
            return nevralgia_render_error(request, 'A diferença entre as sessões precisa ser entre 8 a 16 dias. Cheque a diferença entre as sessões 3 e 4.', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        elif check_future(nova_data_4_1, nova_data_5_1) not in range(8,16):
            return nevralgia_render_error(request, 'A diferença entre as sessões precisa ser entre 8 a 16 dias. Cheque a diferença entre as sessões 4 e 5.', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        elif check_future(nova_data_5_1, nova_data_6_1) not in range(8,16):
            return nevralgia_render_error(request, 'A diferença entre as sessões precisa ser entre 8 a 16 dias. Cheque a diferença entre as sessões 5 e 6.', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        elif check_future(nova_data_6_1, nova_data_7_1) not in range(8,16):
            return nevralgia_render_error(request, 'A diferença entre as sessões precisa ser entre 8 a 16 dias. Cheque a diferença entre as sessões 6 e 7.', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        elif check_future(nova_data_7_1, nova_data_8_1) not in range(8,16):
            return nevralgia_render_error(request, 'A diferença entre as sessões precisa ser entre 8 a 16 dias. Cheque a diferença entre as sessões 7 e 8.', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        elif check_future(nova_data_8_1, nova_data_9_1) not in range(8,16):
            return nevralgia_render_error(request, 'A diferença entre as sessões precisa ser entre 8 a 16 dias. Cheque a diferença entre as sessões 8 e 9.', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        elif check_future(nova_data_9_1, nova_data_10_1) not in range(8,16):
            return nevralgia_render_error(request, 'A diferença entre as sessões precisa ser entre 8 a 16 dias. Cheque a diferença entre as sessões 9 e 10.', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        elif check_future(nova_data_10_1, nova_data_11_1) not in range(8,16):
            return nevralgia_render_error(request, 'A diferença entre as sessões precisa ser entre 8 a 16 dias. Cheque a diferença entre as sessões 10 e 11.', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        elif check_future(nova_data_11_1, nova_data_12_1) not in range(8,16):
            return nevralgia_render_error(request, 'A diferença entre as sessões precisa ser entre 8 a 16 dias. Cheque a diferença entre as sessões 11 e 12.', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        elif check_future(nova_data_12_1, nova_data_13_1) not in range(8,16):
            return nevralgia_render_error(request, 'A diferença entre as sessões precisa ser entre 8 a 16 dias. Cheque a diferença entre as sessões 12 e 13.', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        elif check_future(nova_data_13_1, nova_data_14_1) not in range(8,16):
            return nevralgia_render_error(request, 'A diferença entre as sessões precisa ser entre 8 a 16 dias. Cheque a diferença entre as sessões 13 e 14.', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        elif check_future(nova_data_14_1, nova_data_15_1) not in range(8,16):
            return nevralgia_render_error(request, 'A diferença entre as sessões precisa ser entre 8 a 16 dias. Cheque a diferença entre as sessões 14 e 15.', medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)

        if Consulta.objects.filter(medico=medico, data__dia=dia_1, data__mes=mes_1, data__ano=ano_1, data__hora=hora_1_1, data__minuto=minuto_1_1).exists():
            error_messages = f'Data 1 inválida: {nova_data_1_1}, esse médico já tem compromisso para esse horário.' 
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
                   
        if Consulta.objects.filter(medico=medico, data__dia=dia_1, data__mes=mes_1, data__ano=ano_1, data__hora=hora_1_2, data__minuto=minuto_1_2).exists():
            error_messages = f'Data 1 inválida: {nova_data_1_1}, esse médico já tem compromisso para esse horário.'
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        
        if Consulta.objects.filter(medico=medico, data__dia=dia_2, data__mes=mes_2, data__ano=ano_2, data__hora=hora_2_1, data__minuto=minuto_2_1).exists():
            error_messages = f'Data 2 inválida: {nova_data_2_1}, esse médico já tem compromisso para esse horário.' 
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)

        if Consulta.objects.filter(medico=medico, data__dia=dia_2, data__mes=mes_2, data__ano=ano_2, data__hora=hora_2_2, data__minuto=minuto_2_2).exists():
            error_messages = f'Data 2 inválida: {nova_data_2_1}, esse médico já tem compromisso para esse horário.'
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)

        if Consulta.objects.filter(medico=medico, data__dia=dia_3, data__mes=mes_3, data__ano=ano_3, data__hora=hora_3_1, data__minuto=minuto_3_1).exists():
            error_messages = f'Data 3 inválida: {nova_data_3_1}, esse médico já tem compromisso para esse horário.' 
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)

        if Consulta.objects.filter(medico=medico, data__dia=dia_3, data__mes=mes_3, data__ano=ano_3, data__hora=hora_3_2, data__minuto=minuto_3_2).exists():
            error_messages = f'Data 3 inválida: {nova_data_3_1}, esse médico já tem compromisso para esse horário.'
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        
        if Consulta.objects.filter(medico=medico, data__dia=dia_4, data__mes=mes_4, data__ano=ano_4, data__hora=hora_4_1, data__minuto=minuto_4_1).exists():
            error_messages = f'Data 4 inválida: {nova_data_4_1}, esse médico já tem compromisso para esse horário.'
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15) 

        if Consulta.objects.filter(medico=medico, data__dia=dia_4, data__mes=mes_4, data__ano=ano_4, data__hora=hora_4_2, data__minuto=minuto_4_2).exists():
            error_messages = f'Data 4 inválida: {nova_data_4_1}, esse médico já tem compromisso para esse horário.'
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)

        if Consulta.objects.filter(medico=medico, data__dia=dia_5, data__mes=mes_5, data__ano=ano_5, data__hora=hora_5_1, data__minuto=minuto_5_1).exists():
            error_messages = f'Data 5 inválida: {nova_data_5_1}, esse médico já tem compromisso para esse horário.' 
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        
        if Consulta.objects.filter(medico=medico, data__dia=dia_5, data__mes=mes_5, data__ano=ano_5, data__hora=hora_5_2, data__minuto=minuto_5_2).exists():
            error_messages = f'Data 5 inválida: {nova_data_5_1}, esse médico já tem compromisso para esse horário.'
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        
        if Consulta.objects.filter(medico=medico, data__dia=dia_6, data__mes=mes_6, data__ano=ano_6, data__hora=hora_6_1, data__minuto=minuto_6_1).exists():
            error_messages = f'Data 6 inválida: {nova_data_6_1}, esse médico já tem compromisso para esse horário.'
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)

        if Consulta.objects.filter(medico=medico, data__dia=dia_6, data__mes=mes_6, data__ano=ano_6, data__hora=hora_6_2, data__minuto=minuto_6_2).exists():
            error_messages = f'Data 6 inválida: {nova_data_6_1}, esse médico já tem compromisso para esse horário.'
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        
        if Consulta.objects.filter(medico=medico, data__dia=dia_7, data__mes=mes_7, data__ano=ano_7, data__hora=hora_7_1, data__minuto=minuto_7_1).exists():
            error_messages = f'Data 7 inválida: {nova_data_7_1}, esse médico já tem compromisso para esse horário.'
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15) 

        if Consulta.objects.filter(medico=medico, data__dia=dia_7, data__mes=mes_7, data__ano=ano_7, data__hora=hora_7_2, data__minuto=minuto_7_2).exists():
            error_messages = f'Data 7 inválida: {nova_data_7_1}, esse médico já tem compromisso para esse horário.'
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        
        if Consulta.objects.filter(medico=medico, data__dia=dia_8, data__mes=mes_8, data__ano=ano_8, data__hora=hora_8_1, data__minuto=minuto_8_1).exists():
            error_messages = f'Data 8 inválida: {nova_data_8_1}, esse médico já tem compromisso para esse horário.'
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15) 

        if Consulta.objects.filter(medico=medico, data__dia=dia_8, data__mes=mes_8, data__ano=ano_8, data__hora=hora_8_2, data__minuto=minuto_8_2).exists():
            error_messages = f'Data 8 inválida: {nova_data_8_1}, esse médico já tem compromisso para esse horário.'
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)

        if Consulta.objects.filter(medico=medico, data__dia=dia_9, data__mes=mes_9, data__ano=ano_9, data__hora=hora_9_1, data__minuto=minuto_9_1).exists():
            error_messages = f'Data 9 inválida: {nova_data_9_1}, esse médico já tem compromisso para esse horário.'
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15) 

        if Consulta.objects.filter(medico=medico, data__dia=dia_9, data__mes=mes_9, data__ano=ano_9, data__hora=hora_9_2, data__minuto=minuto_9_2).exists():
            error_messages = f'Data 9 inválida: {nova_data_9_1}, esse médico já tem compromisso para esse horário.'
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        
        if Consulta.objects.filter(medico=medico, data__dia=dia_10, data__mes=mes_10, data__ano=ano_10, data__hora=hora_10_1, data__minuto=minuto_10_1).exists():
            error_messages = f'Data 10 inválida: {nova_data_10_1}, esse médico já tem compromisso para esse horário.' 
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)

        if Consulta.objects.filter(medico=medico, data__dia=dia_10, data__mes=mes_10, data__ano=ano_10, data__hora=hora_10_2, data__minuto=minuto_10_2).exists():
            error_messages = f'Data 10 inválida: {nova_data_10_1}, esse médico já tem compromisso para esse horário.'
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        
        if Consulta.objects.filter(medico=medico, data__dia=dia_11, data__mes=mes_11, data__ano=ano_11, data__hora=hora_11_1, data__minuto=minuto_11_1).exists():
            error_messages = f'Data 11 inválida: {nova_data_11_1}, esse médico já tem compromisso para esse horário.'
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)

        if Consulta.objects.filter(medico=medico, data__dia=dia_11, data__mes=mes_11, data__ano=ano_11, data__hora=hora_11_2, data__minuto=minuto_11_2).exists():
            error_messages = f'Data 11 inválida: {nova_data_11_1}, esse médico já tem compromisso para esse horário.'
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        
        if Consulta.objects.filter(medico=medico, data__dia=dia_12, data__mes=mes_12, data__ano=ano_12, data__hora=hora_12_1, data__minuto=minuto_12_1).exists():
            error_messages = f'Data 12 inválida: {nova_data_12_1}, esse médico já tem compromisso para esse horário.'
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15) 

        if Consulta.objects.filter(medico=medico, data__dia=dia_12, data__mes=mes_12, data__ano=ano_12, data__hora=hora_12_2, data__minuto=minuto_12_2).exists():
            error_messages = f'Data 12 inválida: {nova_data_12_1}, esse médico já tem compromisso para esse horário.'
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        
        if Consulta.objects.filter(medico=medico, data__dia=dia_13, data__mes=mes_13, data__ano=ano_13, data__hora=hora_13_1, data__minuto=minuto_13_1).exists():
            error_messages = f'Data 13 inválida: {nova_data_13_1}, esse médico já tem compromisso para esse horário.'
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15) 

        if Consulta.objects.filter(medico=medico, data__dia=dia_13, data__mes=mes_13, data__ano=ano_13, data__hora=hora_13_2, data__minuto=minuto_13_2).exists():
            error_messages = f'Data 13 inválida: {nova_data_13_1}, esse médico já tem compromisso para esse horário.'
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)

        if Consulta.objects.filter(medico=medico, data__dia=dia_14, data__mes=mes_14, data__ano=ano_14, data__hora=hora_14_1, data__minuto=minuto_14_1).exists():
            error_messages = f'Data 14 inválida: {nova_data_14_1}, esse médico já tem compromisso para esse horário.'
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15) 

        if Consulta.objects.filter(medico=medico, data__dia=dia_14, data__mes=mes_14, data__ano=ano_14, data__hora=hora_14_2, data__minuto=minuto_14_2).exists():
            error_messages = f'Data 14 inválida: {nova_data_14_1}, esse médico já tem compromisso para esse horário.'
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        
        if Consulta.objects.filter(medico=medico, data__dia=dia_15, data__mes=mes_15, data__ano=ano_15, data__hora=hora_15_1, data__minuto=minuto_15_1).exists():
            error_messages = f'Data 15 inválida: {nova_data_15_1}, esse médico já tem compromisso para esse horário.'
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15) 

        if Consulta.objects.filter(medico=medico, data__dia=dia_15, data__mes=mes_15, data__ano=ano_15, data__hora=hora_15_2, data__minuto=minuto_15_2).exists():
            error_messages = f'Data 15 inválida: {nova_data_15_1}, esse médico já tem compromisso para esse horário.'
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
                
        try:
            consulta1_1 = Consulta.objects.create(paciente=paciente, servico='nevralgia', medico=medico, data=nova_data_1_1)
            consulta1_1.save()
            consulta1_2 = Consulta.objects.create(paciente=paciente, servico='nevralgia', medico=medico, data=nova_data_1_2, ehParte2=True)
            consulta1_2.save()
            consulta2_1 = Consulta.objects.create(paciente=paciente, servico='nevralgia', medico=medico, data=nova_data_2_1)
            consulta2_1.save()
            consulta2_2 = Consulta.objects.create(paciente=paciente, servico='nevralgia', medico=medico, data=nova_data_2_2, ehParte2=True)
            consulta2_2.save()
            consulta3_1 = Consulta.objects.create(paciente=paciente, servico='nevralgia', medico=medico, data=nova_data_3_1)
            consulta3_1.save()
            consulta3_2 = Consulta.objects.create(paciente=paciente, servico='nevralgia', medico=medico, data=nova_data_3_2, ehParte2=True)
            consulta3_2.save()
            consulta4_1 = Consulta.objects.create(paciente=paciente, servico='nevralgia', medico=medico, data=nova_data_4_1)
            consulta4_1.save()
            consulta4_2 = Consulta.objects.create(paciente=paciente, servico='nevralgia', medico=medico, data=nova_data_4_2, ehParte2=True)
            consulta4_2.save()
            consulta5_1 = Consulta.objects.create(paciente=paciente, servico='nevralgia', medico=medico, data=nova_data_5_1)
            consulta5_1.save()
            consulta5_2 = Consulta.objects.create(paciente=paciente, servico='nevralgia', medico=medico, data=nova_data_5_2, ehParte2=True)
            consulta5_2.save()
            consulta6_1 = Consulta.objects.create(paciente=paciente, servico='nevralgia', medico=medico, data=nova_data_6_1)
            consulta6_1.save()
            consulta6_2 = Consulta.objects.create(paciente=paciente, servico='nevralgia', medico=medico, data=nova_data_6_2, ehParte2=True)
            consulta6_2.save()
            consulta7_1 = Consulta.objects.create(paciente=paciente, servico='nevralgia', medico=medico, data=nova_data_7_1)
            consulta7_1.save()
            consulta7_2 = Consulta.objects.create(paciente=paciente, servico='nevralgia', medico=medico, data=nova_data_7_2, ehParte2=True)
            consulta7_2.save()
            consulta8_1 = Consulta.objects.create(paciente=paciente, servico='nevralgia', medico=medico, data=nova_data_8_1)
            consulta8_1.save()
            consulta8_2 = Consulta.objects.create(paciente=paciente, servico='nevralgia', medico=medico, data=nova_data_8_2, ehParte2=True)
            consulta8_2.save()
            consulta9_1 = Consulta.objects.create(paciente=paciente, servico='nevralgia', medico=medico, data=nova_data_9_1)
            consulta9_1.save()
            consulta9_2 = Consulta.objects.create(paciente=paciente, servico='nevralgia', medico=medico, data=nova_data_9_2, ehParte2=True)
            consulta9_2.save()
            consulta10_1 = Consulta.objects.create(paciente=paciente, servico='nevralgia', medico=medico, data=nova_data_10_1)
            consulta10_1.save()
            consulta10_2 = Consulta.objects.create(paciente=paciente, servico='nevralgia', medico=medico, data=nova_data_10_2, ehParte2=True)
            consulta10_2.save()
            consulta11_1 = Consulta.objects.create(paciente=paciente, servico='nevralgia', medico=medico, data=nova_data_11_1)
            consulta11_1.save()
            consulta11_2 = Consulta.objects.create(paciente=paciente, servico='nevralgia', medico=medico, data=nova_data_11_2, ehParte2=True)
            consulta11_2.save()
            consulta12_1 = Consulta.objects.create(paciente=paciente, servico='nevralgia', medico=medico, data=nova_data_12_1)
            consulta12_1.save()
            consulta12_2 = Consulta.objects.create(paciente=paciente, servico='nevralgia', medico=medico, data=nova_data_12_2, ehParte2=True)
            consulta12_2.save()
            consulta13_1 = Consulta.objects.create(paciente=paciente, servico='nevralgia', medico=medico, data=nova_data_13_1)
            consulta13_1.save()
            consulta13_2 = Consulta.objects.create(paciente=paciente, servico='nevralgia', medico=medico, data=nova_data_13_2, ehParte2=True)
            consulta13_2.save()
            consulta14_1 = Consulta.objects.create(paciente=paciente, servico='nevralgia', medico=medico, data=nova_data_14_1)
            consulta14_1.save()
            consulta14_2 = Consulta.objects.create(paciente=paciente, servico='nevralgia', medico=medico, data=nova_data_14_2, ehParte2=True)
            consulta14_2.save()
            consulta15_1 = Consulta.objects.create(paciente=paciente, servico='nevralgia', medico=medico, data=nova_data_15_1)
            consulta15_1.save()
            consulta15_2 = Consulta.objects.create(paciente=paciente, servico='nevralgia', medico=medico, data=nova_data_15_2, ehParte2=True)
            consulta15_2.save()
        except:
            error_messages = 'Algo deu errado :/ Tente novamente'
            return nevralgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10, data_11, horario_11, data_12, horario_12, data_13, horario_13, data_14, horario_14, data_15, horario_15)
        
        messages.success(request, f'Tratamento de Pós-Cirurgia: {paciente} com {medico.nome_completo} - Marcado com sucesso')
        return redirect('dashboard')
    else:
        context = {
                'horarios': time_choices,
                'medicos': Medico.objects.all().filter(nevralgia=True),
            }
        return render(request, 'consultas/nevralgia.html', context)