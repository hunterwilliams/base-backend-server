from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from user_manager.forms import (
    UserAdminCreationForm,
    UserAdminChangeForm,
)
from user_manager.models import User, Profile

from config.helpers import model_admin_url


class UserAdminView(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = (
        "email",
        "is_superuser",
        "is_active",
    )
    list_filter = ("is_superuser", "is_active")
    readonly_fields = (
        "id",
        "is_superuser",
    )
    fieldsets = (
        (None, {"fields": ("id", "email", "password")}),
        ("Permissions", {"fields": ("groups",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = ()


class ProfileAdminView(admin.ModelAdmin):
    model = Profile
    list_display = ("__str__", "user_link", "first_name", "last_name")

    search_fields = ("user__email", "first_name", "last_name")
    autocomplete_fields = ["user"]

    def user_link(self, obj):
        return model_admin_url(obj.user)


admin.site.register(User, UserAdminView)
admin.site.register(Profile, ProfileAdminView)

admin.site.site_header = "User Administration"
admin.site.site_title = "User Admin"
