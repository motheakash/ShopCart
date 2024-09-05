from typing import Optional, Any
from django.utils import timezone
from django.db.models import QuerySet
from .models import Member


class MemberService:
    @staticmethod
    def create_member(data: dict[str, any]) -> Member:
        return Member.objects.create(**data)
    
    @staticmethod
    def get_all_members() -> QuerySet[Member]:
        return Member.objects.all()
    
    @staticmethod
    def get_member_by_id(member_id: int) -> Optional[Member]:
        return Member.objects.filter(member_id=member_id).first()
    
    @staticmethod
    def update_member(member: Member, data: dict[str, any]) -> Member:
        for attr, value in data.items():
            setattr(member, attr, value)
        member.save()
        return member
    
    @staticmethod
    def delete_member(member: Member) -> None:
        member.deleted_at = timezone.now()
        member.save()

    @staticmethod
    def get_member_by_active_state(active: bool) -> Optional[Member]:
        return Member.objects.filter(active=active)