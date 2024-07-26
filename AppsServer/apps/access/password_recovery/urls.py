from django.urls import path, include
from . import views

urlpatterns = [
    path('recovery/user/', views.ValidateUserAPI.as_view(), name='get_user_login'),
    path('recovery/code/', views.ValidateCodeAPI.as_view(), name='get_user_code'),
    path('recovery/password/', views.RefreshPasswordAPI.as_view(), name='get_new_password'),
]
