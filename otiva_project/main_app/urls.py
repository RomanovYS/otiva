from django.urls import path
import main_app.views as main_app

urlpatterns = [
    path('', main_app.MainPageView.as_view(), name='main_page'),
]
