from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/', views.SignUpAPIView.as_view(), name='add_user'),
]