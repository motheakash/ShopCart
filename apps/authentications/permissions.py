from rest_framework.permissions import BasePermission
from apps.member_management.models import Member
from apps.core.utils import replace_numbers
from config.settings.base import SIMPLE_JWT
from functools import wraps
from django.http import HttpResponseForbidden
from apps.authentications.models import MemberRole, RolePermission, Role, Permission
import jwt




class IsAuthenticated(BasePermission):
    """
    Custom permission to check if the user is authenticated using JWT tokens.
    """

    def has_permission(self, request, view):
        token = request.headers.get('Authorization')

        if token is None:
            return False

        try:
            decoded_token = jwt.decode(token, SIMPLE_JWT['SECRETE_KEY'], algorithms=SIMPLE_JWT['JWT_ALGORITHM'])
            request.user = Member.objects.get(member_id=decoded_token['user_id'])
            return True
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False
        except Member.DoesNotExist:
            return False


def is_authorized(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        endpoint = replace_numbers(request.path)
        method = request.method
        user = request.user

        has_permission = RolePermission.objects.filter(
            role__memberrole__member=user,
            permission__endpoint=endpoint,
            permission__method=method
        ).exists()
        
        if not has_permission:
            return HttpResponseForbidden("Access denied!")
        
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view

