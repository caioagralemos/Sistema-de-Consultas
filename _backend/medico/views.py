from django.shortcuts import render, redirect
from django.contrib import messages, auth
from consultas.models import Consulta

from django.db.models import F

# Create your views here.

def dashboard(request):
    context = {
        'consultas': Consulta.objects.all().filter(medico=request.user.medico, ehParte2=False).order_by('data__data_hora_completa'),
    }
    return render(request, 'medico/dashboard.html', context)

def login(request):
    return render(request, 'medico/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'Você fez logout com sucesso!')
        return redirect('index')