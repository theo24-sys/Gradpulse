from django.urls import path
from . import views

urlpatterns = [
    path('', views.market_simulations_list, name='market_simulations_list'),
    path('<int:pk>/workspace/', views.market_simulation_workspace, name='market_simulation_workspace'),
    path('match/', views.trigger_matching, name='trigger_matching'),
    path('<int:pk>/progress/', views.simulation_progress_update, name='simulation_progress_update'),
]
