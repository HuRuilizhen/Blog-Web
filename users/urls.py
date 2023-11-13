from django.contrib import admin
from django.urls import path, re_path
from .views import *

urlpatterns = [
    path("", home_view, name="home"),
    path("home/", home_view, name="home"),
    re_path("^user_home/(?P<user_id>\d+)/$", user_home_view, name="user_home"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("signup/", signup_view, name="signup"),
    path("edit_profile/", edit_profile_view, name="edit_profile"),
    path(
        "edit_profile_user_photo_url/",
        edit_profile_user_photo_url_view,
        name="edit_profile_user_photo_url",
    ),
    path(
        "edit_profile_user_description/",
        edit_profile_user_description_view,
        name="edit_profile_user_description",
    ),
    path(
        "edit_profile_personal_homepage/",
        edit_profile_personal_homepage_view,
        name="edit_profile_personal_homepage",
    ),
    path(
        "edit_profile_password/",
        edit_profile_password_view,
        name="edit_profile_password",
    ),
    path("ranklist/", ranklist_view, name="ranklist"),
]
