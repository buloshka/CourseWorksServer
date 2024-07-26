from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.SignInAPI.as_view(), name='get_user_data'),
]