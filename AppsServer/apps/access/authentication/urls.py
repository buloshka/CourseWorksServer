from django.urls import path, include
from . import views

urlpatterns = [
    path('signin/', views.SignInAPIView.as_view(), name='get_user'),
]