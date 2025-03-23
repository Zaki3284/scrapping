from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
from .models import FormL,RegistrationLog,LoginLog



@admin.register(FormL)
class FormLogAdmin(admin.ModelAdmin):
    list_display = ('form_type', 'timestamp')
    search_fields = ('form_type', 'data')
    list_filter = ('form_type', 'timestamp')
    
@admin.register(RegistrationLog)
class RegistrationLogAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'password', 'created_at')
    search_fields = ('name', 'email', 'phone_number')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)  # Make created_at read-only

# Register the LoginLog model
@admin.register(LoginLog)
class LoginLogAdmin(admin.ModelAdmin):
    list_display = ('email', 'password', 'login_time')
    search_fields = ('email',)
    list_filter = ('login_time',)
    readonly_fields = ('login_time',)  # Make login_time read-only

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('name', 'email', 'phone_number', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'name', 'phone_number')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2')}),
        ('Personal info', {'fields': ('name', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    filter_horizontal = ('user_permissions',)

admin.site.register(CustomUser, CustomUserAdmin)



# !admin
# Email: iscae@gmail.com
# Phone number: 44444444
# Password: jaffar1234

# !User
# mail:jsdellaly@gmail.com 
# pas:iscae1234

  