from consultas.choices import time_choices
from medico.models import Medico
from django.shortcuts import render, redirect
from django.contrib import messages

def nevralgia_render_error(request, message, medico, data_1='', horario_1='', data_2='', horario_2='', data_3='', horario_3='', data_4='', horario_4='', data_5='', horario_5='', data_6='', horario_6='', data_7='', horario_7='', data_8='', horario_8='', data_9='', horario_9='', data_10='', horario_10='', data_11='', horario_11='', data_12='', horario_12='', data_13='', horario_13='', data_14='', horario_14='', data_15='', horario_15=''):
    context = {
        'medico_escolhido': medico,
        'horarios': time_choices,
        'medicos': Medico.objects.all().filter(pos_cirurgia=True),
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
        'data7': data_7,
        'horario7': horario_7,
        'data8': data_8,
        'horario8': horario_8,
        'data9': data_9,
        'horario9': horario_9,
        'data10': data_10,
        'horario10': horario_10,
        'data11': data_11,
        'horario11': horario_11,
        'data12': data_12,
        'horario12': horario_12,
        'data13': data_13,
        'horario13': horario_13,
        'data14': data_14,
        'horario14': horario_14,
        'data15': data_15,
        'horario15': horario_15,
    }
    messages.error(request, message)
    return render(request, 'consultas/nevralgia.html', context)