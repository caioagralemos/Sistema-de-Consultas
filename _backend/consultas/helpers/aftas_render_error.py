from consultas.choices import time_choices
from medico.models import Medico
from django.shortcuts import render, redirect
from django.contrib import messages

def aftas_render_error(request, message, medico_user='', data_1='', horario_1='', data_2='', horario_2='', data_3='', horario_3='', data_4='', horario_4=''):
    context = {
        'medico': medico_user,
        'horarios': time_choices,
        'medicos': Medico.objects.all().filter(consulta=True),
        'data_1': data_1,
        'horario_1': horario_1,
        'data_2': data_2,
        'horario_2': horario_2,
        'data_3': data_3,
        'horario_3': horario_3,
        'data_4': data_4,
        'horario_4': horario_4,
    }
    messages.error(request, message)
    return render(request, 'consultas/aftas.html', context)