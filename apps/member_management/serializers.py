from typing import Any, Dict
from rest_framework import serializers
from .models import Member, Address
from config.settings.base import MAX_ADDRESSES

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


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        exclude = ('deleted_at', 'created_at', 'updated_at')

    def validate(self, attrs):
        member_id = attrs.get('member_id')
        addresses = Address.objects.filter(member_id=member_id).values('address_id').count()
        
        if addresses > MAX_ADDRESSES:
            raise serializers.ValidationError(f'maximum address limit reached.')

        return super().validate(attrs)