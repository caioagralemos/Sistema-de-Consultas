from consultas.choices import time_choices
from medico.models import Medico
from django.shortcuts import render, redirect
from django.contrib import messages

def consulta_render_error(request, message, medico_user='', data='', horario=''):
    context = {
        'medico': medico_user,
        'horarios': time_choices,
        'medicos': Medico.objects.all().filter(consulta=True),
        'data': data,
        'horario': horario,
    }
    messages.error(request, message)
    return render(request, 'consultas/marcar_consulta.html', context)