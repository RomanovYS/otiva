from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from django.shortcuts import render
from django.urls import path, include


# как заглушку использую, потом уберу
def index(request):
    return render(request, 'index.html')
    

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('user_app.urls')),
    path('ads/', include('advertisement_app.urls')),
#     path('', index),
    path('', include('main_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
