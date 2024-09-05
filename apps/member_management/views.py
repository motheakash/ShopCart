from typing import Any, Union, List
from django.db.models import QuerySet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from .serializers import MemberSerializer
from .models import Member
from .services import MemberService
from apps.core.utils import CustomPagination
from apps.authentications.permissions import IsAuthenticated, is_authorized
from django.utils.decorators import method_decorator



class MemberAPIView(ListCreateAPIView):
    pagination_class = CustomPagination
    serializer_class = MemberSerializer
    service_class = MemberService
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> Union[QuerySet[Member], List[Member]]:
        """
        Return the list of members. This method can be overridden or extended.
        """
        active = self.request.query_params.get('active', None)
        if active is not None:
            return self.service_class.get_member_by_active_state(bool(int(active)))
        return self.service_class.get_all_members()

    @method_decorator(is_authorized)
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Handle GET requests, retrieve the paginated list of members, and return the response.
        """
        try:
            page_size: int = int(request.GET.get('page_size', 10))
            paginator: CustomPagination = self.pagination_class()
            paginator.page_size = page_size

            queryset = self.get_queryset()
            paginated_queryset = paginator.paginate_queryset(queryset, request)
            serializer = self.serializer_class(paginated_queryset, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_404_NOT_FOUND)

    @method_decorator(is_authorized)
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Handle POST requests, validate and save the member, and return the response.
        """
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                self.perform_create(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer: MemberSerializer) -> None:
        """
        Save the new member instance. This can be overridden for custom save logic.
        """
        serializer.save()


class MemberByIdView(RetrieveDestroyAPIView):
    serializer_class = MemberSerializer
    service_class = MemberService
    permission_classes = [IsAuthenticated]

    def get_object(self) -> Member:
        """
        Retrieve the member object based on the provided ID.
        """
        member_id = self.kwargs.get('member_id')
        if not member_id:
            raise NotFound('Member ID not provided.')
        member = self.service_class.get_member_by_id(member_id)
        if not member:
            raise NotFound('Member not found.')
        return member
    
    @method_decorator(is_authorized)
    def retrieve(self, request, *args, **kwargs) -> Response:
        """
        Handle GET requests to retrieve a member by ID.
        """
        try:
            member = self.get_object()
            if not member.active:
                raise PermissionDenied('Member is not active.')
            serializer = self.serializer_class(member)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_404_NOT_FOUND)
    
    @method_decorator(is_authorized)
    def delete(self, request, *args, **kwargs) -> Response:
        """
        Handle DELETE requests to delete a member by ID.
        """
        try:
            member = self.get_object()
            if not member.active:
                raise PermissionDenied('Cannot delete inactive member.')
            member.delete()
            return Response({'message': 'Member deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_404_NOT_FOUND)