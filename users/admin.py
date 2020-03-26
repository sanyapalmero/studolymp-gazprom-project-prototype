from django.contrib import admin, auth

from .models import User

admin.site.unregister(auth.models.Group)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'role', 'created_at')
