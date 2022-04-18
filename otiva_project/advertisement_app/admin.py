from django.contrib import admin

from advertisement_app.models import TechAdvertisement, TechPhoto


@admin.register(TechAdvertisement)
class TechAdvertisementAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'condition', 'price', 'placement_period', 'creator']


@admin.register(TechPhoto)
class TechPhotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'photo']
