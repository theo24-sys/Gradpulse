from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('unismart/role-selection/', views.unismart_role_selection, name='unismart_role_selection'),
    path('unismart/dashboard/', views.unismart_dashboard, name='unismart_dashboard'),
    path('unismart/chat/', views.unismart_chat, name='unismart_chat'),
    path('unismart/helb/', views.unismart_helb_guide, name='unismart_helb_guide'),
    path('unismart/kcse-entry/', views.unismart_kcse_entry, name='unismart_kcse_entry'),
    path('unismart/save-kcse/', views.unismart_save_kcse, name='unismart_save_kcse'),
    path('unismart/cart/', views.unismart_manage_cart, name='unismart_manage_cart'),
    path('unismart/courses/', views.unismart_course_browser, name='unismart_course_browser'),
    path('unismart/extract/<int:resource_id>/', views.unismart_extract_courses, name='unismart_extract_courses'),
    path('unismart/add-to-cart/', views.unismart_add_to_cart, name='unismart_add_to_cart'),
    path('unismart/remove-from-cart/<int:item_id>/', views.unismart_remove_from_cart, name='unismart_remove_from_cart'),
]
