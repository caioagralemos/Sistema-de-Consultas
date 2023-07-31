from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from consultas.models import Consulta

# Create your views here.

def dashboard(request):
    context = {
        'consultas': Consulta.objects.all().filter(medico=request.user.medico),
    }
    return render(request, 'medico/dashboard.html', context)

def login(request):
    return render(request, 'medico/login.html')

def logout(request):
    return redirect('index')