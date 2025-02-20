from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, EmergencyContact, PoliceStation, SOSRequest
from django.utils.html import format_html
from django.urls import reverse
from .models import SOSRequest


if admin.site.is_registered(SOSRequest):
    admin.site.unregister(SOSRequest)

@admin.register(SOSRequest)
class SOSRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'get_location_link', 'is_active')
    list_filter = ('is_active', 'timestamp')
    search_fields = ('user__username',)
    readonly_fields = ('get_location_link',)

    def get_location_link(self, obj):
        url = obj.get_google_maps_link()
        if url:
            return format_html('<a href="{}" target="_blank">View on Google Maps</a>', url)
        return "No location data"
    get_location_link.short_description = 'Location'
    get_location_link.allow_tags = True
    

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'is_verified', 'is_active')
    list_filter = ('is_verified', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email', 'phone', 'aadhar')}),
        ('Permissions', {'fields': ('is_verified', 'is_active', 'is_staff')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone', 'password1', 'password2'),
        }),
    )
    search_fields = ('username', 'email', 'phone')
    ordering = ('username',)
    actions = ['approve_users']

    def approve_users(self, request, queryset):
        queryset.update(is_verified=True)
    approve_users.short_description = "Approve selected users"

# Unregister if already registered (safety check)
if admin.site.is_registered(CustomUser):
    admin.site.unregister(CustomUser)

# Register models
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(EmergencyContact)
admin.site.register(PoliceStation)