from django.urls import path, URLPattern
from typing import List
from .views import ProductAPI

urlpatterns: List[URLPattern] = [
    path('products/', ProductAPI.as_view(), name='product')
]