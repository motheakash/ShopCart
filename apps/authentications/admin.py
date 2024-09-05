from django.contrib import admin
from django import forms
from .models import Permission, Role, RolePermission, MemberRole
from config.settings.local import ROLE_PERMISSIONS

class PermissionAdminForm(forms.ModelForm):
    class Meta:
        model = Permission
        exclude = ('deleted_at', )

    def clean(self):
        cleaned_data = super().clean()
        method = cleaned_data.get('method')
        
        if method.upper() not in ROLE_PERMISSIONS['Admin']:
            raise forms.ValidationError(f'Method is not valid. Please choose from {ROLE_PERMISSIONS['Admin']}')

        return cleaned_data


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    form = PermissionAdminForm
    list_display = ('id', 'endpoint', 'description', 'created_at', 'updated_at')
    search_fields = ('endpoint', 'description')
    list_filter = ('created_at', 'updated_at')
    exclude = ('deleted_at', )

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'role', 'created_at', 'updated_at')
    search_fields = ('role',)
    list_filter = ('created_at', 'updated_at')
    exclude = ('deleted_at', )

class RolePermissionAdminForm(forms.ModelForm):
    class Meta:
        model = RolePermission
        exclude = ('deleted_at', )
    
    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role').role
        method = cleaned_data.get('permission').method

        if method not in ROLE_PERMISSIONS[role]:
            raise forms.ValidationError(f'Cannot assign {method} method to {role}')

        return cleaned_data

@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    form = RolePermissionAdminForm
    list_display = ('id', 'role', 'permission', 'created_at', 'updated_at')
    search_fields = ('role__role', 'permission__endpoint')
    list_filter = ('created_at', 'updated_at')
    # raw_id_fields = ('role', 'permission')
    exclude = ('deleted_at', )

@admin.register(MemberRole)
class MemberRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'member', 'role', 'created_at', 'updated_at')
    search_fields = ('member__member_id', 'role__role')
    list_filter = ('created_at', 'updated_at')
    raw_id_fields = ('member', 'role')
    exclude = ('deleted_at', )
