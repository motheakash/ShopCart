from typing import Any, Dict
from rest_framework import serializers
from apps.member_management.models import Member
from .services import LoginService


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs:dict) -> dict:
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            try:
                member = Member.objects.get(username=username)
            except Member.DoesNotExist:
                raise serializers.ValidationError('Member not found with username.')
            if not LoginService().check_password(password, member.password):
                raise serializers.ValidationError('Password not matched.')
            if not member.active:
                raise serializers.ValidationError('Member is not active.')
        
        else:
            raise serializers.ValidationError('Must include "username" and "password".')

        attrs['member'] = member
        return attrs