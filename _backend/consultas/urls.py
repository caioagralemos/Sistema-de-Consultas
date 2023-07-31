from django.urls import path
from . import views

urlpatterns = [
    path('', views.consulta, name='agendarconsulta'),
    path('aftas', views.aftas, name='aftas'),
    path('hipersensibilidade', views.hipersensibilidade, name='hipersensibilidade'), 
    path('pos_cirurgia', views.pos_cirurgia, name='pos_cirurgia'),
    path('nevralgia', views.nevralgia, name='nevralgia'), 
    path('lesoes', views.lesoes, name='lesoes'),
]