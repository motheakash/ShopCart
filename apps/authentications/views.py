from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from typing import Any, Dict
from .services import LoginService
from .serializers import LoginSerializer
from apps.member_management.serializers import MemberSerializer



class LoginView(APIView):
    serializer_class = LoginSerializer
    member_seralizer = MemberSerializer
    service_class = LoginService

    def post(self, request: Any, *args: Any, **kwargs: Any) -> Response:
        """
        Handle POST requests for user login.
        """
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            member = serializer.validated_data['member']
            token = self.service_class.generate_access_token(member)
            return Response({
                'member': self.member_seralizer(member).data,
                'token': token
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
