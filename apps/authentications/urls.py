from django.urls import path, URLPattern
from typing import List
from .views import LoginView

urlpatterns: List[URLPattern] = [
    path('login/', LoginView.as_view(), name='login-member'),
]