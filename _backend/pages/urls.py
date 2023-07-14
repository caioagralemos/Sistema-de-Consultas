from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # homepage
    path('agendarconsulta', views.agendar_consulta, name='agendarconsulta'), # agendar consulta
    path('about', views.about, name='about'), # about
]