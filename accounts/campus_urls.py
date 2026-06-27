from django.urls import path, include
from . import views

urlpatterns = [
    path('dashboard/', views.campus_dashboard, name='campus_dashboard'),
    path('profile/', views.campus_profile, name='campus_profile'),
    path('transcript-upload/', views.transcript_upload, name='transcript_upload'),
    path('dashboard/simulations/', include('simulations.urls')),
]
