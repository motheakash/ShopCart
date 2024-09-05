from typing import Any, Dict
from rest_framework import serializers
from .models import Member

class MemberSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Member
        exclude = ('deleted_at', )
    def create(self, validated_data: Dict[str, Any]) -> Member:
        """
        Override to set default values and create a new member object.
        """
        password = validated_data.get('password', None)
        if password and len(password) > 16:
            raise serializers.ValidationError({'message': 'Password length cannot exceed 16 characters.'})

        validated_data['active'] = False  # Ensure 'active' field is set to False by default
        return super().create(validated_data)
