from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, 'pages/index.html')

def agendar_consulta(request):
    return render(request, 'pages/marcar_consulta.html')


def about(request):
    return render(request, 'pages/about.html')