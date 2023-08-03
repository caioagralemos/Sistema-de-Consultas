from django.shortcuts import render, redirect
from django.contrib import messages, auth
from consultas.models import Consulta

from datetime import datetime

from django.db.models import F

# Create your views here.

def dashboard(request):
    context = {
        'consultas': Consulta.objects.all().filter(medico=request.user.medico, ehParte2=False, data__data_hora_completa__gte=datetime.now()).order_by('data__data_hora_completa'),
    }
    return render(request, 'medico/dashboard.html', context)

def consultas_passadas(request):
    context = {
        'consultas': Consulta.objects.filter(medico=request.user.medico, ehParte2=False, data__data_hora_completa__lt=datetime.now()).order_by('data__data_hora_completa'),
    }
    return render(request, 'medico/consultas_passadas.html', context)

def login(request):
    return render(request, 'medico/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'Você fez logout com sucesso!')
        return redirect('index')