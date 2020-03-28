from django.contrib import admin, auth
from django.contrib.auth.admin import UserAdmin

from .models import User

admin.site.unregister(auth.models.Group)


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'role', 'employer', 'created_at')
    search_fields = ('email', 'username', 'role')
    readonly_fields = ('created_at', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Return users with role=ROLE_EMPLOYER for employer dropdown"""
        if db_field.name == "employer":
            kwargs["queryset"] = User.objects.filter(role=User.ROLE_EMPLOYER)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(User, CustomUserAdmin)
