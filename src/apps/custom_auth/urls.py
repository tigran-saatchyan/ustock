from django.urls import path
from .views import UserInfoView, LoginView

urlpatterns = [
    path('user/', UserInfoView.as_view(), name='user-info'),
    path('login/', LoginView.as_view(), name='login'),
]