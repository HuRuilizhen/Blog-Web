from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("", home_view, name="home"),
    path("home/", home_view, name="home"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("signup/", signup_view, name="signup"),
]
