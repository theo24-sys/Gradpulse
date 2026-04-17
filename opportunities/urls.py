from django.urls import path
from . import views

urlpatterns = [
    path('', views.opportunity_list, name='opportunity_list'),
    path('<int:pk>/', views.opportunity_detail, name='opportunity_detail'),
    path('<int:pk>/apply/', views.apply_opportunity, name='apply_opportunity'),
    path('post/', views.post_opportunity, name='post_opportunity'),
    path('<int:pk>/edit/', views.edit_opportunity, name='edit_opportunity'),
    path('youth-programs/', views.youth_programs_list, name='youth_programs_list'),
    path('scrape-discovery/', views.scrape_discovery, name='scrape_discovery'),
]
