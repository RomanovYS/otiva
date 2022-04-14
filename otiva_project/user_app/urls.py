from django.urls import path
from . import views

app_name = 'user_app'

urlpatterns = [
    path("login/", views.OtivaUserLoginView.as_view(), name='login'),
    path("logout/", views.OtivaUserLogoutView.as_view(), name='logout'),
    path("register/", views.OtivaUserRegisterView.as_view(), name='register'),
]