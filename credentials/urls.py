from django.urls import path
from . import views

urlpatterns = [
    path('', views.credentials_list, name='credentials_list'),
    path('<int:pk>/enroll/', views.enroll_credential, name='enroll_credential'),
    path('simulations/', views.simulations_list, name='simulations_list'),
    path('simulations/premium/', views.premium_upgrade, name='premium_upgrade'),
    path('simulations/manage/', views.manage_simulations, name='manage_simulations'),
    path('simulations/create/', views.simulation_create, name='simulation_create'),
    path('simulations/generate-ai/', views.simulation_generate_ai, name='simulation_generate_ai'),
    path('simulations/<int:pk>/play/', views.simulation_play, name='simulation_play'),
    path('qualifications/', views.qualifications_list, name='qualifications_list'),
]
