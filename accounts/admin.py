from accounts.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.contrib import admin
from accounts.models import *


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('phone_number', 'is_admin', 'is_active', 'get_jalali_date')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('phone_number', 'fullname', 'password',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2'),
        }),
    )
    search_fields = ('phone_number', 'fullname')
    ordering = ('phone_number', 'date_joined')
    filter_horizontal = ()

    def has_add_permission(self, req):
        if req.user.is_admin:
            return True
        return False

    def has_change_permission(self, req, obj=None):
        if req.user.is_admin:
            return True
        return False

    def has_delete_permission(self, req, obj=None):
        if req.user.is_admin:
            return True
        return False


admin.site.unregister(Group)


@admin.register(Otp)
class OtpAdmin(admin.ModelAdmin):

    # Only admin can delete an OTP object
    def has_delete_permission(self, request, obj=None):
        if not request.user.is_admin:
            return False
        return True

    # Only admin can change an OTP object
    def has_change_permission(self, request, obj=None):
        if not request.user.is_admin:
            return False
        return True

    # Only admin can delete OTP objects
    def has_add_permission(self, request):
        if not request.user.is_admin:
            return False
        return True


admin.site.register(EditedUser)
