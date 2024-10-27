from django.contrib import admin
from .models import Member, Address

# Register your models here.
class MemberAdmin(admin.ModelAdmin):
    list_display = ('custom_member_id', 'username', 'email')
    exclude = ('deleted_at',)

    def custom_member_id(self, obj):
        return f"{obj.member_id}-member"

    custom_member_id.short_description = 'Member Id'


class AddressAdmin(admin.ModelAdmin):
    list_display = ('address_id', 'memberid', 'street_address', 'address_type')
    exclude = ('deleted_at', )

    def memberid(self, obj):
        return obj.member_id.username


admin.site.register(Member, MemberAdmin)
admin.site.register(Address, AddressAdmin)