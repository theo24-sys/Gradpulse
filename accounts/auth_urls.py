from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('guest-login/<str:portal>/', views.guest_login, name='guest_login'),
    path('logout/', views.logout_view, name='logout'),
]
