from django.urls import path
from . import views

urlpatterns = [
    path('get/', views.GetUserProfileAPI.as_view(), name='get_user_data'),
    path('buy/', views.BuySubscriptionAPI.as_view(), name='buy_sub'),
]