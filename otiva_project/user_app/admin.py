from django.contrib import admin

from user_app.models import OtivaUser, Role, Country, Area, City, Postcode, Street, MetroLine, Metro, Address, Profile


@admin.register(OtivaUser)
class OtivaUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'username', 'user_type', 'is_active']
    list_display_links = ['id', 'email']
    list_filter = ['user_type']


admin.site.register(Profile)

admin.site.register(Role)
admin.site.register(Country)
admin.site.register(Area)
admin.site.register(City)
admin.site.register(Postcode)
admin.site.register(Street)
admin.site.register(MetroLine)
admin.site.register(Metro)
admin.site.register(Address)
