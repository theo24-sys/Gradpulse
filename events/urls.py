from django.urls import path
from . import views

urlpatterns = [
    path('', views.events_list, name='events_list'),
    path('<int:pk>/rsvp/', views.rsvp_event, name='rsvp_event'),
]
