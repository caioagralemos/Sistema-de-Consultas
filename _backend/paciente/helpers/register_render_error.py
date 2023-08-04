from django.shortcuts import render
from django.contrib import messages

def register_render_error(request, message, first_name='', last_name='', email='', username='', cpf='', aftas='', consulta='', pos_cirurgia='', hipersensibilidade='', nevralgia='', lesoes=''):
    context = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'username': username,
        'cpf': cpf,
        'aftas': aftas,
        'consulta': consulta,
        'pos_cirurgia': pos_cirurgia,
        'hipersensibilidade': hipersensibilidade,
        'nevralgia': nevralgia,
        'lesoes': lesoes,
    }
    messages.error(request, message)
    return render(request, 'paciente/register.html', context)