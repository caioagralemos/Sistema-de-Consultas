from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.dashboard, name='medico-dashboard'),
    path('login', views.login, name='medico-login'),
    path('logout', views.logout, name='medico-logout'), 
]