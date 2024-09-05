from django.urls import path, URLPattern
from typing import List
from .views import MemberAPIView, MemberByIdView

urlpatterns: List[URLPattern] = [
    path('members/', MemberAPIView.as_view(), name='member'),
    path('member/<int:member_id>/', MemberByIdView.as_view(), name='member-by-id'),
]