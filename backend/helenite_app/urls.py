from django.urls import path

from helenite_app import views

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login_endpoint"),
    path("logout/", views.LogoutView.as_view(), name="logout_endpoint"),
    path("register/", views.RegisterCreateAPIView.as_view(), name="register_new_user"),
    path("feed/", views.FeedListCreateAPIView.as_view(), name="feed_endpoint"),
    path("search/", views.SearchListView.as_view(), name="search_endpoint"),
    path("feed/discover/", views.DiscoverListAPIView.as_view(), name="discover_endpoint"),
    path("profile/<slug:custom_slug_profile>/", views.ProfileRetriveAPIView.as_view(), name="profile_info_endpoint"),
    path("profile/<slug:custom_slug_profile>/friends/", views.FriendsListAPIView.as_view(), name="profile_friends_endpoint"),
    path("profile/<slug:custom_slug_profile>/change-settings/", views.ChangeSettingsAPIView.as_view(), name="change_settings_endpoint"),
    path("profile/post/<slug:post_slug>/", views.PostRetriveCreateDeleteAPIView.as_view(), name="single_post_endpoint"),
]
