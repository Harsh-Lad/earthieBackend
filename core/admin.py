from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from .models import HomeSlider, HomeBlock, Products, Categories, Collections

class CustomUserAdmin(UserAdmin):
    """Define admin model for custom User model with no username field."""
    fieldsets = (
        (None, {'fields': ('email', 'password', 'is_verified','token','phone')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','is_verified','token','phone'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_verified', 'token' ,'is_staff')
    search_fields = ('email', 'first_name', 'last_name','is_verified', 'token')
    ordering = ('email',)


admin.site.register(get_user_model(), CustomUserAdmin)

admin.site.register(HomeSlider)
admin.site.register(HomeBlock)
admin.site.register(Products)
admin.site.register(Categories)
admin.site.register(Collections)