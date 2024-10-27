from django.urls import path, URLPattern
from typing import List
from .views import (
    MemberAPIView,
    MemberByIdView,
    Addressview
)

urlpatterns: List[URLPattern] = [
    path('members/', MemberAPIView.as_view(), name='member'),
    path('member/<int:member_id>/', MemberByIdView.as_view(), name='member-by-id'),
    path('member/address/<int:member_id>/', Addressview.as_view(), name='member-address'),
    path('member/address/<int:member_id>/<int:address_id>/', Addressview.as_view(), name='member-address'),
]