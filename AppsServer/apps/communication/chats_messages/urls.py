from django.urls import path
from . import views

urlpatterns = [
    path('get/', views.GetChatsMessagesAPI.as_view(), name='get_messages'),
    path('create/', views.CreateMessageAPI.as_view(), name='create_message'),
    path('edit/', views.EditMessageAPI.as_view(), name='edit_message'),
    path('delete/', views.DeleteMessageAPI.as_view(), name='delete_message'),
]