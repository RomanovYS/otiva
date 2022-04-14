from django.contrib import admin

from user_app.models import OtivaUser


@admin.register(OtivaUser)
class OtivaUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'username', 'user_type', 'is_active']
    list_display_links = ['id', 'email']
    list_filter = ['user_type']
    
    