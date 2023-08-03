from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('dashboard/consultas_passadas', views.consultas_passadas, name='consultas_passadas'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'), 
    path('register', views.register, name='register'),
]