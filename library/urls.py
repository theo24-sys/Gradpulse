from django.urls import path
from . import views

urlpatterns = [
    path('', views.library_list, name='library_list'),
    path('upload/', views.upload_item, name='library_upload'),
    path('item/<int:pk>/', views.item_detail, name='library_item_detail'),
    path('delete/<int:pk>/', views.delete_item, name='library_delete'),
]
