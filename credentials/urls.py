from django.urls import path
from . import views

urlpatterns = [
    path('', views.credentials_list, name='credentials_list'),
    path('<int:pk>/enroll/', views.enroll_credential, name='enroll_credential'),
    path('simulations/', views.simulations_list, name='simulations_list'),
    path('premium-upgrade/', views.premium_upgrade, name='premium_upgrade'),
]
