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
        hora = int(horario[0:2])
        minuto = int(horario[2:])

        try:
            nova_data = Data.objects.create(ano=ano, mes=mes, dia=dia, hora=hora, minuto=minuto)
            nova_data.clean()
            nova_data.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
            return consulta_render_error(request, error_messages, medico, data, horario)
        
        if Consulta.objects.all().filter(medico=medico, data__dia=dia, data__mes=mes, data__ano=ano, data__hora=hora, data__minuto=minuto).exists():
            message = f'Data inválida: {nova_data}, esse médico já tem compromisso para esse horário.'
            return consulta_render_error(request, message, medico, data, horario)
        
        try:
            consulta = Consulta.objects.create(paciente=paciente, servico='consulta', medico=medico, data=nova_data)
            consulta.save()
        except:
            consulta_render_error(request, 'Algo deu errado :/ Tente novamente', medico, data, horario)
        

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

        try:
            nova_data_1 = Data.objects.create(ano=ano_1, mes=mes_1, dia=dia_1, hora=hora_1, minuto=minuto_1)
            nova_data_1.clean()
            nova_data_1.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
            return aftas_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4)

        try:
            nova_data_2 = Data.objects.create(ano=ano_2, mes=mes_2, dia=dia_2, hora=hora_2, minuto=minuto_2)
            nova_data_2.clean()
            nova_data_2.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
            return aftas_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4)

        try:
            nova_data_3 = Data.objects.create(ano=ano_3, mes=mes_3, dia=dia_3, hora=hora_3, minuto=minuto_3)
            nova_data_3.clean()
            nova_data_3.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
            return aftas_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4)

        try:
            nova_data_4 = Data.objects.create(ano=ano_4, mes=mes_4, dia=dia_4, hora=hora_4, minuto=minuto_4)
            nova_data_4.clean()
            nova_data_4.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
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

        try:
            nova_data_1 = Data.objects.create(ano=ano_1, mes=mes_1, dia=dia_1, hora=hora_1, minuto=minuto_1)
            nova_data_1.clean()
            nova_data_1.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
            return hipersensibilidade_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6)

        try:
            nova_data_2 = Data.objects.create(ano=ano_2, mes=mes_2, dia=dia_2, hora=hora_2, minuto=minuto_2)
            nova_data_2.clean()
            nova_data_2.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
            return hipersensibilidade_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6)

        try:
            nova_data_3 = Data.objects.create(ano=ano_3, mes=mes_3, dia=dia_3, hora=hora_3, minuto=minuto_3)
            nova_data_3.clean()
            nova_data_3.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
            return hipersensibilidade_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6)

        try:
            nova_data_4 = Data.objects.create(ano=ano_4, mes=mes_4, dia=dia_4, hora=hora_4, minuto=minuto_4)
            nova_data_4.clean()
            nova_data_4.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
            return hipersensibilidade_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6)

        try:
            nova_data_5 = Data.objects.create(ano=ano_5, mes=mes_5, dia=dia_5, hora=hora_5, minuto=minuto_5)
            nova_data_5.clean()
            nova_data_5.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
            return hipersensibilidade_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6)

        try:
            nova_data_6 = Data.objects.create(ano=ano_6, mes=mes_6, dia=dia_6, hora=hora_6, minuto=minuto_6)
            nova_data_6.clean()
            nova_data_6.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
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

        try:
            nova_data_1 = Data.objects.create(ano=ano_1, mes=mes_1, dia=dia_1, hora=hora_1, minuto=minuto_1)
            nova_data_1.clean()
            nova_data_1.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
            return lesoes_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8)

        try:
            nova_data_2 = Data.objects.create(ano=ano_2, mes=mes_2, dia=dia_2, hora=hora_2, minuto=minuto_2)
            nova_data_2.clean()
            nova_data_2.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
            return lesoes_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8)

        try:
            nova_data_3 = Data.objects.create(ano=ano_3, mes=mes_3, dia=dia_3, hora=hora_3, minuto=minuto_3)
            nova_data_3.clean()
            nova_data_3.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
            return lesoes_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8)

        try:
            nova_data_4 = Data.objects.create(ano=ano_4, mes=mes_4, dia=dia_4, hora=hora_4, minuto=minuto_4)
            nova_data_4.clean()
            nova_data_4.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
            return lesoes_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8)

        try:
            nova_data_5 = Data.objects.create(ano=ano_5, mes=mes_5, dia=dia_5, hora=hora_5, minuto=minuto_5)
            nova_data_5.clean()
            nova_data_5.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
            return lesoes_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8)

        try:
            nova_data_6 = Data.objects.create(ano=ano_6, mes=mes_6, dia=dia_6, hora=hora_6, minuto=minuto_6)
            nova_data_6.clean()
            nova_data_6.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
            return lesoes_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8)

        try:
            nova_data_7 = Data.objects.create(ano=ano_7, mes=mes_7, dia=dia_7, hora=hora_7, minuto=minuto_7)
            nova_data_7.clean()
            nova_data_7.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
            return lesoes_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8)

        try:
            nova_data_8 = Data.objects.create(ano=ano_8, mes=mes_8, dia=dia_8, hora=hora_8, minuto=minuto_8)
            nova_data_8.clean()
            nova_data_8.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
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
            error_messages = ', '.join(e.messages)
            return pos_cirurgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10)

        try:
            nova_data_2 = Data.objects.create(ano=ano_2, mes=mes_2, dia=dia_2, hora=hora_2, minuto=minuto_2)
            nova_data_2.clean()
            nova_data_2.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
            return pos_cirurgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10)

        try:
            nova_data_3 = Data.objects.create(ano=ano_3, mes=mes_3, dia=dia_3, hora=hora_3, minuto=minuto_3)
            nova_data_3.clean()
            nova_data_3.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
            return pos_cirurgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10)

        try:
            nova_data_4 = Data.objects.create(ano=ano_4, mes=mes_4, dia=dia_4, hora=hora_4, minuto=minuto_4)
            nova_data_4.clean()
            nova_data_4.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
            return pos_cirurgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10)

        try:
            nova_data_5 = Data.objects.create(ano=ano_5, mes=mes_5, dia=dia_5, hora=hora_5, minuto=minuto_5)
            nova_data_5.clean()
            nova_data_5.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
            return pos_cirurgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10)

        try:
            nova_data_6 = Data.objects.create(ano=ano_6, mes=mes_6, dia=dia_6, hora=hora_6, minuto=minuto_6)
            nova_data_6.clean()
            nova_data_6.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
            return pos_cirurgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10)

        try:
            nova_data_7 = Data.objects.create(ano=ano_7, mes=mes_7, dia=dia_7, hora=hora_7, minuto=minuto_7)
            nova_data_7.clean()
            nova_data_7.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
            return pos_cirurgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10)

        try:
            nova_data_8 = Data.objects.create(ano=ano_8, mes=mes_8, dia=dia_8, hora=hora_8, minuto=minuto_8)
            nova_data_8.clean()
            nova_data_8.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
            return pos_cirurgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10)

        try:
            nova_data_9 = Data.objects.create(ano=ano_9, mes=mes_9, dia=dia_9, hora=hora_9, minuto=minuto_9)
            nova_data_9.clean()
            nova_data_9.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
            return pos_cirurgia_render_error(request, error_messages, medico, data_1, horario_1, data_2, horario_2, data_3, horario_3, data_4, horario_4, data_5, horario_5, data_6, horario_6, data_7, horario_7, data_8, horario_8, data_9, horario_9, data_10, horario_10)
        
        try:
            nova_data_10 = Data.objects.create(ano=ano_10, mes=mes_10, dia=dia_10, hora=hora_10, minuto=minuto_10)
            nova_data_10.clean()
            nova_data_10.save()
        except ValidationError as e:
            error_messages = ', '.join(e.messages)
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