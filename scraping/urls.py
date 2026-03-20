from django.urls import path
from . import views

urlpatterns = [
    path('external/opportunities/', views.external_opportunities, name='external_opportunities'),
    path('external/events/', views.external_events, name='external_events'),
    path('external/learning/', views.external_learning, name='external_learning'),
]
