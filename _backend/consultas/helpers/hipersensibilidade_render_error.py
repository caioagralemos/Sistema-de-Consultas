from consultas.choices import time_choices
from medico.models import Medico
from django.shortcuts import render, redirect
from django.contrib import messages

def hipersensibilidade_render_error(request, message, medico, data_1='', horario_1='', data_2='', horario_2='', data_3='', horario_3='', data_4='', horario_4='', data_5='', horario_5='', data_6='', horario_6=''):
    context = {
        'medico_escolhido': medico,
        'horarios': time_choices,
        'medicos': Medico.objects.all().filter(hipersensibilidade=True),
        'data1': data_1,
        'horario1': horario_1,
        'data2': data_2,
        'horario2': horario_2,
        'data3': data_3,
        'horario3': horario_3,
        'data4': data_4,
        'horario4': horario_4,
        'data5': data_5,
        'horario5': horario_5,
        'data6': data_6,
        'horario6': horario_6,
    }
    messages.error(request, message)
    return render(request, 'consultas/hipersensibilidade.html', context)