from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html

class CustomUserAdmin(BaseUserAdmin):
    # ... (your existing class definition) ...
    list_display = (
        'username', 'email', 'full_name', 'status_badge', 
        'date_joined', 'password'
    )

    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-is_superuser', '-is_staff', 'username')

    fieldsets = (
        ('Informations personnelles', {
            'fields': ('username', 'email', 'first_name', 'last_name')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Informations importantes', {
            'fields': ('last_login', 'date_joined', 'password')
        }),
    )

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = "Nom complet"

    def status_badge(self, obj):
        if obj.is_superuser:
            color = 'red'
            text = 'Superuser'
        elif obj.is_staff:
            color = 'blue'
            text = 'Staff'
        else:
            color = 'gray'
            text = 'Utilisateur'
        return format_html(
            '<span style="padding:2px 8px; background-color:{}; color:white; border-radius:4px;">{}</span>',
            color, text
        )
    status_badge.short_description = 'Statut'
    status_badge.admin_order_field = 'is_superuser'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('-is_superuser', '-is_staff', 'username')

# Unregister the default User model, then register your custom one.
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass
finally:
    admin.site.register(User, CustomUserAdmin)