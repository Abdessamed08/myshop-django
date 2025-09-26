from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User  # ⚡ on importe ton User custom

class CustomUserAdmin(BaseUserAdmin):
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

    # Affiche prénom + nom
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = "Nom complet"

    # Badge pour le statut
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

# On enregistre directement ton User custom
admin.site.register(User, CustomUserAdmin)
