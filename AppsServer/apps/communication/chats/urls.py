from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.GetAllChatsAPI.as_view(), name='get_all_chats'),
    path('get_all/', views.GetChatsAPI.as_view(), name='get_users_chats'),
    path('get_one/', views.GetChatAPI.as_view(), name='get_chat'),
    path('create/', views.CreateSingleChatAPI.as_view(), name='create_chat'),
    path('delete/', views.DeleteChatAPI.as_view(), name='delete_chat'),
]