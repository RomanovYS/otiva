from django.urls import path
from .views import TechAdvertisementCreateView, TechAdvertisementDetailView, TechAdvertisementEditView

app_name = 'advertisement_app'

urlpatterns = [
    path('ad/<slug:slug>/', TechAdvertisementDetailView.as_view(), name='tech_ad_detail'),
    path('create/', TechAdvertisementCreateView.as_view(), name='tech_ad_create'),
    path('ad/<slug:slug>/edit/', TechAdvertisementEditView.as_view(), name='tech_ad_edit'),
]
