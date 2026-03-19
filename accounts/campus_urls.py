from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.campus_dashboard, name='campus_dashboard'),
    path('profile/', views.campus_profile, name='campus_profile'),
]
