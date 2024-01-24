from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.LoginAPIView.as_view(), name='get_user'),
]