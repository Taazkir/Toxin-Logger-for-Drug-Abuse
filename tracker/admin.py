from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        'username', 'email', 'name', 'height', 'weight', 'phone_number',
        'gender', 'bac', 'cigarette_toxins', 'alcohol_toxins',
        'total_alcohol', 'total_cigarettes',
        'is_staff', 'is_active',
    )
    list_filter = ('username', 'email', 'name', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {
            'fields': (
                'name', 'height', 'weight', 'phone_number', 'gender',
                'bac', 'cigarette_toxins', 'alcohol_toxins',
                'total_alcohol', 'total_cigarettes',  # Include these fields in the detail view
            ),
        }),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'name', 'height', 'weight', 'phone_number',
                'gender', 'bac', 'cigarette_toxins', 'alcohol_toxins',
                'password1', 'password2'
            ),
        }),
    )
    search_fields = ('username', 'email', 'name',)
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(CustomUser, CustomUserAdmin)
