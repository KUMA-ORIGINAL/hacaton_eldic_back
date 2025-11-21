from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group

from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from common.base_admin import BaseModelAdmin
from ..models import User

admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(GroupAdmin, BaseModelAdmin):
    pass


@admin.register(User)
class UserAdmin(UserAdmin, BaseModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "phone_number",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    model = User
    autocomplete_fields = ("groups",)

    ordering = ('-date_joined',)
    list_display = ('id', 'phone_number', 'email', 'full_name', 'is_active', )
    list_display_links = ('id', 'phone_number')
