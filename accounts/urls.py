from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('unismart/role-selection/', views.unismart_role_selection, name='unismart_role_selection'),
    path('unismart/dashboard/', views.unismart_dashboard, name='unismart_dashboard'),
    path('unismart/chat/', views.unismart_chat, name='unismart_chat'),
]
