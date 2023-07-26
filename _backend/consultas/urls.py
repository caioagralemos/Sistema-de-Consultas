from django.urls import path
from . import views

urlpatterns = [
    path('', views.agendar_consulta, name='agendarconsulta'), # agendar consulta
    path('confirmacao', views.confirmacao, name='confirmacao'), # pag de confirmação
]