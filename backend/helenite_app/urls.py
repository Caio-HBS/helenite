from django.contrib import admin
from django.urls import path


urlpatterns = [
    path("login/", name="login_endpoint"),
    path("register/", name="register_new_user"),
    path("feed/", name="feed_endpoint"),
    path("feed/discover/", name="discover_endpoint"),
    path("profile/<int:pk>/", name="profile_info_endpoint"),
    path("profile/<int:pk>/change-settings", name="change_settings_endpoint"),
]
