from django.urls import path
from . import views

urlpatterns = [
    path('', views.networking_view, name='networking'),
    path('connect/<int:pk>/', views.send_connection, name='send_connection'),
    path('accept/<int:pk>/', views.accept_connection, name='accept_connection'),
    path('collaborations/', views.collaborations_view, name='collaborations'),
    path('inbox/', views.inbox_view, name='inbox'),
    path('chat/<int:pk>/', views.chat_detail_view, name='chat_detail'),
    path('delete-message/<int:msg_pk>/', views.delete_message_view, name='delete_message'),
]
