from django.contrib import admin
from .models import Member

# Register your models here.
class MemberAdmin(admin.ModelAdmin):
    list_display = ('custom_member_id', 'username', 'email')
    exclude = ('deleted_at',)

    def custom_member_id(self, obj):
        return f"{obj.member_id}-member"

    custom_member_id.short_description = 'Member Id'


admin.site.register(Member, MemberAdmin)