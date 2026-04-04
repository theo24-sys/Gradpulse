from django.urls import path
from . import views

urlpatterns = [
    path('', views.grades_view, name='grades'),
    path('api/transcripts/upload/', views.upload_transcript, name='upload_transcript'),
]
