from django.shortcuts import render, redirect
from django.contrib import messages
from medico.models import Medico

# Create your views here.

def agendar_consulta(request):
    if request.method == 'POST':
        paciente = request.user.paciente
        medico = request.get['medico']
        data = request.get['data']
        messages.success(request, f'{data}')
        return redirect('index')
    else:
        context = {
            'medicos': Medico.objects.all(),
        }
        return render(request, 'consultas/marcar_consulta.html', context)

def confirmacao(request):
    return render(request, 'consultas/confirmacao.html')