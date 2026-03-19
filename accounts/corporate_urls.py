from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.corporate_dashboard, name='corporate_dashboard'),
    path('profile/', views.corporate_profile, name='corporate_profile'),
    path('talent/', views.talent_search, name='talent_search'),
    path('applications/', views.corporate_applications, name='corporate_applications'),
    path('applications/<int:pk>/status/', views.update_application_status, name='update_application_status'),
]
