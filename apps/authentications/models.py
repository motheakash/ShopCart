from django.db import models
from django.utils import timezone
from apps.core.models import SoftDeleteManager, BaseModel
from apps.member_management.models import Member


class Permission(BaseModel):
    id = models.AutoField(db_column='Id', primary_key=True)
    endpoint = models.CharField(db_column='Endpoint', max_length=100)
    method = models.CharField(db_column='Method', max_length=10)
    description = models.CharField(db_column='Description', max_length=300, blank=True, null=True)

    objects = SoftDeleteManager()

    class Meta:
        db_table = 'Permissions'
        unique_together = (('endpoint', 'method'),)

    def __str__(self):
        return f"{self.method}-{self.endpoint}"

class Role(BaseModel):
    id = models.AutoField(db_column='Id', primary_key=True)
    role = models.CharField(db_column='Role', max_length=100, unique=True)

    objects = SoftDeleteManager()

    class Meta:
        db_table = 'Roles'

    def __str__(self):
        return self.role

class RolePermission(BaseModel):
    id = models.AutoField(db_column='Id', primary_key=True)
    role = models.ForeignKey(Role, db_column='RoleId', on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, db_column='PermissionId', on_delete=models.CASCADE)

    objects = SoftDeleteManager()

    class Meta:
        db_table = 'RolePermissions'
        unique_together = (('role', 'permission'),)

    def __str__(self):
        return f'Role: {self.role.role}, Permission: {self.permission.endpoint}'


class MemberRole(BaseModel):
    id = models.AutoField(db_column='Id', primary_key=True)
    role = models.ForeignKey(Role, db_column='RoleId', on_delete=models.CASCADE)
    member = models.ForeignKey(Member, db_column='MemberId', on_delete=models.CASCADE)

    class Meta:
        db_table = 'MemberRoles'
        unique_together = (('role', 'member'),)

    def __str__(self):
        return f'Member: {self.member.member_id}, Role: {self.role.role}'
