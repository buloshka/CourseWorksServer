from django.urls import path
from . import views

urlpatterns = [
    path('create_chat/', views.CreateGroupAPI.as_view(), name='create_group_chat'),
]